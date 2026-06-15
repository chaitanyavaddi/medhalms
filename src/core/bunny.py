import re
import os
import secrets
import ssl
import urllib.request
import urllib.error

from django.conf import settings


def slugify_filename(name):
    stem, ext = os.path.splitext(name)
    slug = re.sub(r'[^\w\s-]', '', stem.lower())
    slug = re.sub(r'[\s_]+', '-', slug)
    slug = re.sub(r'-{2,}', '-', slug).strip('-')
    slug = slug[:60] or 'file'
    suffix = secrets.token_hex(4)
    return f"{slug}-{suffix}{ext.lower()}"


def upload_file(file_obj, subdomain):
    """Upload a Django InMemoryUploadedFile to Bunny storage.

    Args:
        file_obj: Django InMemoryUploadedFile with .name, .content_type, .read(), .size
        subdomain: blog subdomain used as the storage path prefix

    Returns:
        cdn_url (str) on success.

    Raises:
        RuntimeError: if Bunny returns an HTTP error.
    """
    filename = slugify_filename(file_obj.name)
    object_path = f"{subdomain}/{filename}"

    endpoint = settings.BUNNY_STORAGE_ENDPOINT.rstrip('/')
    zone = settings.BUNNY_STORAGE_ZONE
    url = f"{endpoint}/{zone}/{object_path}"
    cdn_url = f"{settings.BUNNY_CDN_BASE}/{object_path}"
    content_type = file_obj.content_type or ''

    print(f"[upload] PUT {url}  key={settings.BUNNY_ACCESS_KEY[:8]}...  size={file_obj.size}  type={content_type}")

    req = urllib.request.Request(
        url,
        data=file_obj.read(),
        method='PUT',
        headers={
            'AccessKey': settings.BUNNY_ACCESS_KEY,
            'Content-Type': content_type,
        },
    )
    ssl_ctx = ssl._create_unverified_context() if settings.DEBUG else None
    try:
        with urllib.request.urlopen(req, context=ssl_ctx) as resp:
            print(f"[upload] Bunny response {resp.status}")
            if resp.status not in (200, 201):
                raise RuntimeError(f"Bunny returned {resp.status}")
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='replace')
        print(f"[upload] HTTPError {e.code}: {body}")
        raise RuntimeError(f"Bunny {e.code}: {body}")

    return cdn_url


def delete_file(object_path):
    endpoint = settings.BUNNY_STORAGE_ENDPOINT.rstrip('/')
    zone     = settings.BUNNY_STORAGE_ZONE
    url      = f"{endpoint}/{zone}/{object_path}"
    req = urllib.request.Request(
        url,
        method='DELETE',
        headers={'AccessKey': settings.BUNNY_ACCESS_KEY},
    )
    ssl_ctx = ssl._create_unverified_context() if settings.DEBUG else None
    try:
        with urllib.request.urlopen(req, context=ssl_ctx):
            pass
    except urllib.error.HTTPError:
        pass
