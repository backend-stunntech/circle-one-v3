from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.tenant_specific_apps.circle_one.users.abstract_models import AbstractUserProfile
from utils.email.send import render_and_send_mail
from utils.media import database_file_upload_path
from utils.models import TimeStampMixin
from utils.tenants import get_current_tenant


class Department(TimeStampMixin, models.Model):
    name = models.CharField(max_length=256)


class Group(TimeStampMixin, models.Model):
    name = models.CharField(max_length=256)
    department = models.ForeignKey(Department, related_name='get_groups', on_delete=models.CASCADE)


class UserProfile(TimeStampMixin, AbstractUserProfile):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='get_profile', on_delete=models.CASCADE)
    require_password_change = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to=database_file_upload_path)

    groups = models.ManyToManyField(Group, related_name='get_users')
    invited_by = models.ForeignKey('users.UserProfile', related_name='invited_users', null=True,
                                   on_delete=models.CASCADE)

    @property
    def is_last_admin(self):
        return self.role == self.ROLE_ADMIN and __class__.objects.filter(role=self.ROLE_ADMIN).count() == 1

    def send_invitation(self, password: str):
        return render_and_send_mail('users/invite-user', {
            'profile': self,
            'password': password,
            'tenant': get_current_tenant(),
        })
