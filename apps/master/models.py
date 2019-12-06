from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.utils.text import slugify
from tenant_schemas.models import TenantMixin
from tenant_schemas.utils import tenant_context


class Tenant(TenantMixin):
    tenant_domain = models.CharField(max_length=256, unique=True, blank=True)
    sub_domain = models.CharField(max_length=256, unique=True, blank=True)

    @classmethod
    def master(cls):
        return __class__.objects.get(tenant_domain='',
                                     sub_domain='', domain_url=settings.MASTER_DOMAIN,
                                     schema_name=settings.MASTER_SCHEMA_NAME)

    @classmethod
    def create_tenant(cls, tenant_domain: str, sub_domain: str) -> 'Tenant':
        domain_url = f"{sub_domain}.{settings.MASTER_DOMAIN}"

        # schema names shall contain alphanumeric and underscores only
        schema_name = slugify(domain_url).replace('-', '_')

        tenant = __class__.objects.create(tenant_domain=tenant_domain,
                                          sub_domain=sub_domain,
                                          domain_url=domain_url,
                                          schema_name=schema_name)
        Site.objects.create(name=tenant_domain, domain=domain_url)
        return tenant
