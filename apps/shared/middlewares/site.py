from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist


class DynamicSiteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        domain = request.get_host().split(":")[0]

        try:
            site = Site.objects.get(domain=domain)
        except ObjectDoesNotExist:
            site = Site.objects.first()
            if site and site.domain != domain:
                site.domain = domain
                site.name = domain
                site.save(update_fields=["domain", "name"])

        request.site = site
        return self.get_response(request)
