from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from core.bunny import upload_file, delete_file


def _org_member_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            main = getattr(settings, "MAIN_DOMAIN", "localhost:8000")
            return redirect(f"http://{main}/login/")
        if not getattr(request, "org", None):
            main = getattr(settings, "MAIN_DOMAIN", "localhost:8000")
            return redirect(f"http://{main}/orgs/")
        from orgs.models import OrgMember
        if not OrgMember.objects.filter(user=request.user, org=request.org).exists():
            main = getattr(settings, "MAIN_DOMAIN", "localhost:8000")
            return redirect(f"http://{main}/orgs/")
        return view_func(request, *args, **kwargs)
    return wrapper


# ── Overview ───────────────────────────────────────────────────────

@_org_member_required
def overview(request):
    ctx = {}
    if request.headers.get('HX-Request'):
        return render(request, 'dashboard/partials/overview_body.html', ctx)
    return render(request, 'dashboard/overview.html', ctx)


# ── Settings ───────────────────────────────────────────────────────

SETTINGS_SECTIONS = {'general', 'appearance', 'domain', 'account', 'danger'}

@_org_member_required
def settings_view(request, section=None):
    from django.http import Http404
    if section is not None and section not in SETTINGS_SECTIONS:
        raise Http404
    from orgs.models import Organization
    org = request.org
    if request.method == 'POST':
        org.name            = request.POST.get('name', '').strip() or org.name
        org.bio             = request.POST.get('bio', '').strip()
        org.brand_primary   = request.POST.get('brand_primary', '').strip() or org.brand_primary
        org.brand_secondary = request.POST.get('brand_secondary', '').strip() or org.brand_secondary
        org.logo_display    = request.POST.get('logo_display', 'name')
        org.nav_sticky      = request.POST.get('nav_sticky', 'none')
        new_domain = request.POST.get('custom_domain', '').strip().lower()
        if new_domain != org.custom_domain:
            org.custom_domain = new_domain
            org.custom_domain_verified = False
        org.save()
        if request.headers.get('HX-Request'):
            ctx = {
                'saved': True,
                'display_choices': Organization._meta.get_field('logo_display').choices,
                'open_section': section,
            }
            return render(request, 'dashboard/partials/settings_body.html', ctx)
        return redirect('dashboard_settings_section', section=section) if section else redirect('dashboard_settings')
    ctx = {
        'display_choices': Organization._meta.get_field('logo_display').choices,
        'open_section': section,
    }
    if request.headers.get('HX-Request'):
        return render(request, 'dashboard/partials/settings_body.html', ctx)
    return render(request, "dashboard/settings.html", ctx)


@_org_member_required
@require_POST
def media_upload(request):
    f = request.FILES.get('file')
    if not f:
        return JsonResponse({'error': 'No file'}, status=400)

    allowed_image = {'image/jpeg', 'image/png', 'image/gif', 'image/webp'}
    allowed_video = {'video/mp4', 'video/webm', 'video/quicktime'}
    content_type = f.content_type or ''
    if content_type not in allowed_image | allowed_video:
        return JsonResponse({'error': 'Unsupported file type'}, status=400)
    if f.size > 200 * 1024 * 1024:
        return JsonResponse({'error': 'File too large (max 200 MB)'}, status=400)

    try:
        cdn_url = upload_file(f, request.org.subdomain)
    except RuntimeError as e:
        return JsonResponse({'error': str(e)}, status=502)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=502)

    return JsonResponse({
        'url':  cdn_url,
        'type': 'image' if content_type in allowed_image else 'video',
    })


@_org_member_required
@require_POST
def media_delete(request):
    url = request.POST.get('url', '').strip()
    if not url:
        return JsonResponse({'error': 'No URL'}, status=400)
    cdn_base = getattr(settings, 'BUNNY_CDN_BASE', '').rstrip('/')
    if not cdn_base or not url.startswith(cdn_base + '/'):
        return JsonResponse({'error': 'Invalid URL'}, status=400)
    object_path = url[len(cdn_base) + 1:]
    try:
        delete_file(object_path)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=502)
    return JsonResponse({'deleted': True})


@_org_member_required
@require_POST
def verify_custom_domain(request):
    org = request.org
    domain = org.custom_domain.strip()
    if not domain:
        return JsonResponse({'error': 'No custom domain set'}, status=400)

    main_domain = getattr(settings, 'MAIN_DOMAIN', 'myapp.com')
    expected_cname = f"{org.subdomain}.{main_domain}"
    verified = False

    try:
        import struct, random, socket as _socket

        def build_dns_query(hostname):
            txid = random.randint(0, 65535)
            flags = 0x0100
            header = struct.pack('>HHHHHH', txid, flags, 1, 0, 0, 0)
            qname = b''
            for part in hostname.rstrip('.').split('.'):
                qname += bytes([len(part)]) + part.encode()
            qname += b'\x00'
            question = qname + struct.pack('>HH', 5, 1)
            return txid, header + question

        def parse_cname_response(data, txid):
            if len(data) < 12: return None
            if struct.unpack('>H', data[:2])[0] != txid: return None
            if struct.unpack('>H', data[6:8])[0] == 0: return None
            pos = 12
            while pos < len(data) and data[pos] != 0:
                if data[pos] & 0xC0 == 0xC0: pos += 2; break
                pos += data[pos] + 1
            else:
                pos += 1
            pos += 4
            if pos >= len(data): return None
            if data[pos] & 0xC0 == 0xC0: pos += 2
            else:
                while pos < len(data) and data[pos] != 0: pos += data[pos] + 1
                pos += 1
            if pos + 10 > len(data): return None
            rtype, _, _, rdlen = struct.unpack('>HHIH', data[pos:pos+10])
            pos += 10
            if rtype != 5: return None
            cname, cpos = [], pos
            while cpos < pos + rdlen and cpos < len(data):
                if data[cpos] & 0xC0 == 0xC0: cpos = struct.unpack('>H', data[cpos:cpos+2])[0] & 0x3FFF; continue
                length = data[cpos]
                if length == 0: break
                cpos += 1
                cname.append(data[cpos:cpos+length].decode('ascii', errors='replace'))
                cpos += length
            return '.'.join(cname)

        sock = _socket.socket(_socket.AF_INET, _socket.SOCK_DGRAM)
        sock.settimeout(4)
        txid, query = build_dns_query(domain)
        sock.sendto(query, ('8.8.8.8', 53))
        response, _ = sock.recvfrom(512)
        sock.close()
        cname = parse_cname_response(response, txid)
        if cname:
            verified = cname.rstrip('.').lower() == expected_cname.rstrip('.').lower()
    except Exception:
        verified = False

    org.custom_domain_verified = verified
    org.save(update_fields=['custom_domain_verified'])
    return JsonResponse({'verified': verified, 'expected_cname': expected_cname})


@_org_member_required
@require_POST
def org_delete(request):
    org = request.org
    org.delete()
    main = getattr(settings, 'MAIN_DOMAIN', 'localhost:8000')
    return redirect(f'http://{main}/orgs/')


@_org_member_required
@require_POST
def logo_upload(request):
    f = request.FILES.get('logo')
    if not f:
        return JsonResponse({'error': 'No file'}, status=400)
    if f.content_type not in {'image/jpeg', 'image/png', 'image/webp', 'image/gif'}:
        return JsonResponse({'error': 'Only JPEG, PNG, WEBP, or GIF allowed'}, status=400)
    if f.size > 5 * 1024 * 1024:
        return JsonResponse({'error': 'Max 5 MB'}, status=400)
    org = request.org
    old_avatar = org.avatar
    try:
        url = upload_file(f, f'{org.subdomain}/logo')
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=502)
    if old_avatar:
        cdn_base = getattr(settings, 'BUNNY_CDN_BASE', '').rstrip('/')
        try:
            delete_file(old_avatar[len(cdn_base):].lstrip('/'))
        except Exception:
            pass
    org.avatar = url
    org.logo_display = 'avatar_name'
    org.save(update_fields=['avatar', 'logo_display'])
    return JsonResponse({'url': url})


@_org_member_required
@require_POST
def logo_delete(request):
    org = request.org
    if org.avatar:
        cdn_base = getattr(settings, 'BUNNY_CDN_BASE', '').rstrip('/')
        try:
            delete_file(org.avatar[len(cdn_base):].lstrip('/'))
        except Exception:
            pass
        org.avatar = ''
        org.save(update_fields=['avatar'])
    return JsonResponse({'ok': True})
