import json
import logging
import urllib.request
import urllib.error

from django.conf import settings

logger = logging.getLogger(__name__)


def purge_org_cache(org):
    subdomain = getattr(org, 'subdomain', '')
    if not subdomain:
        return
    main_domain = getattr(settings, 'MAIN_DOMAIN', 'myapp.com')
    base = f'https://{subdomain}.{main_domain}'
    purge_urls([f'{base}/', f'{base}/favicon.svg'])


def purge_urls(urls):
    token = getattr(settings, 'CLOUDFLARE_API_TOKEN', '')
    zone_id = getattr(settings, 'CLOUDFLARE_ZONE_ID', '')
    if not token or not zone_id or not urls:
        return
    data = json.dumps({'files': urls}).encode()
    req = urllib.request.Request(
        f'https://api.cloudflare.com/client/v4/zones/{zone_id}/purge_cache',
        data=data,
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        },
        method='POST',
    )
    try:
        with urllib.request.urlopen(req, timeout=5):
            pass
    except Exception as e:
        logger.warning('Cloudflare purge failed: %s', e)
