from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver

from CircleOneV3.utils import get_current_schema_name


class UserProfile(models.Model):
    ROLE_AGENT = 'agent'
    ROLE_MANAGER = 'manager'
    ROLE_ADMIN = 'admin'
    ROLE_CHOICES = (
        (ROLE_AGENT, 'Agent'),
        (ROLE_MANAGER, 'Manager'),
        (ROLE_ADMIN, 'Admin')
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='get_profile', on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)

    def is_owned_by(self, user):
        return True


@receiver(models.signals.post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile_on_user_creation(sender, instance, created, **kwargs):
    if created and get_current_schema_name() != 'public':
        try:
            UserProfile.objects.get(user=instance)
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=instance, role=UserProfile.ROLE_AGENT)
