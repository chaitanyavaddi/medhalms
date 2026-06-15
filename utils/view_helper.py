from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse


def redirect_to(request, url_or_name):
    if request.headers.get("HX-Request"):
        r = HttpResponse()
        url = url_or_name if url_or_name.startswith(('/', 'http')) else reverse(url_or_name)
        r["HX-Redirect"] = url
        return r
    return redirect(url_or_name)


class HtmxInfo:
    def __init__(self, request):
        h = request.headers
        self.request      = bool(h.get("HX-Request"))
        self.target       = h.get("HX-Target")
        self.trigger      = h.get("HX-Trigger")
        self.trigger_name = h.get("HX-Trigger-Name")
        self.current_url  = h.get("HX-Current-URL")

    def __bool__(self):
        return self.request


def htmx(request):
    return HtmxInfo(request)


def page_range(page_obj, window=2):
    """Compact page list for pagination. 0 = ellipsis gap."""
    total   = page_obj.paginator.num_pages
    current = page_obj.number
    pages   = sorted({1, total} | set(range(max(1, current - window), min(total, current + window) + 1)))
    result, prev = [], None
    for p in pages:
        if prev and p - prev > 1:
            result.append(0)
        result.append(p)
        prev = p
    return result
