from urllib.parse import urlparse
from accounts.models import Membership
from core.models import Organization

ORG_HEADER = "X-Org"  # fallback if you aren't using subdomains

def get_org_from_request(request):
    # 1) Try subdomain: tenant.example.com
    host = request.get_host().split(':')[0]
    parts = host.split('.')
    if len(parts) > 2:  # naive: <sub>.<domain>.<tld>
        sub = parts[0]
        try:
            return Organization.objects.get(slug=sub)
        except Organization.DoesNotExist:
            pass
    # 2) Fallback header
    slug = request.headers.get(ORG_HEADER)
    if slug:
        try:
            return Organization.objects.get(slug=slug)
        except Organization.DoesNotExist:
            pass
    # 3) Fallback: if authenticated, use primary membership org
    if request.user and request.user.is_authenticated:
        m = Membership.objects.filter(user=request.user).select_related('organization').first()
        return m.organization if m else None
    return None