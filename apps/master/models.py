from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.db.transaction import atomic
from django.urls import reverse
from django.utils.text import slugify
from tenant_schemas.models import TenantMixin
from tenant_schemas.utils import tenant_context

from apps.tenant_specific_apps.circle_one.users.models import UserProfile
from utils.email.send import render_and_send_mail
from utils.models import TimeStampMixin


class Tenant(TimeStampMixin, TenantMixin):
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
        with atomic():
            tenant = __class__.objects.create(tenant_domain=tenant_domain,
                                              sub_domain=sub_domain,
                                              domain_url=domain_url,
                                              schema_name=schema_name)
            Site.objects.create(name=tenant_domain, domain=domain_url)
            return tenant

    @property
    def default_sender_email(self):
        return f"{settings.DEFAULT_SENDER_EMAIL}@{self.domain_url}"

    @property
    def frontend_domain(self):
        return f"{self.sub_domain}.{settings.FRONTEND_MASTER_DOMAIN}"

    @property
    def login_link(self):
        return f"https://{self.frontend_domain}/login"


class SignUpRequest(TimeStampMixin, models.Model):
    tenant_domain = models.CharField(max_length=256)
    sub_domain = models.CharField(max_length=256)
    verification_token = models.UUIDField()

    admin_username = models.EmailField()
    password = models.CharField(max_length=256)

    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    phone = models.CharField(max_length=256)

    @classmethod
    def verify(cls, verification_token, admin_username):
        try:
            request = cls.objects.get(verification_token=verification_token, admin_username=admin_username)
        except cls.DoesNotExist:
            raise PermissionError
        else:
            tenant = Tenant.create_tenant(request.tenant_domain, request.sub_domain)
            with tenant_context(tenant):
                with atomic():
                    admin = User.objects.create(username=request.admin_username,
                                                email=request.admin_username,
                                                is_active=True,
                                                is_staff=True)
                    admin.set_password(request.password)
                    admin.save()
                    admin.get_profile.role = UserProfile.ROLE_ADMIN
                    admin.get_profile.save()
                    return tenant

    @property
    def verification_link(self):
        return (f"https://{settings.MASTER_DOMAIN}"
                f"{reverse('signup-verification')}"
                f"?username={self.admin_username}&verification_token={self.verification_token}")

    def send_verification_email(self):
        return render_and_send_mail('signup/verify-signup', {
            'request': self
        }, recipient=self.admin_username)
