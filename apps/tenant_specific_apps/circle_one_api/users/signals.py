from django.conf import settings
from django.db import models
from django.dispatch import receiver

from apps.tenant_specific_apps.circle_one_api.users.models import UserProfile
from utils.media import delete_old_model_files, rename_model_files_from_field_verbose_name, delete_model_files
from utils.tenants import get_current_schema_name


@receiver(models.signals.post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile_on_user_creation(sender, instance, created, **kwargs):
    if created and get_current_schema_name() != 'public':
        try:
            UserProfile.objects.get(user=instance)
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=instance, role=UserProfile.ROLE_AGENT)


models_with_file_upload = (UserProfile,)
for model in models_with_file_upload:
    models.signals.pre_save.connect(delete_old_model_files, sender=model)
    models.signals.post_save.connect(rename_model_files_from_field_verbose_name, sender=model)
    models.signals.post_delete.connect(delete_model_files, sender=model)
