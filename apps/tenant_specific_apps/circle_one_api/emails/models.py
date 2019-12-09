from django.contrib.postgres.fields import JSONField
from django.db import models

from apps.tenant_specific_apps.circle_one_api.customers.models import Action
from utils.media import database_file_upload_path
from utils.models import TimeStampMixin


class Thread(TimeStampMixin, models.Model):
    action = models.OneToOneField(Action, related_name='get_thread', on_delete=models.CASCADE)

    original_subject = models.CharField(max_length=256)
    from_email = models.EmailField()
    to_email = models.EmailField()


class Attachment(TimeStampMixin, models.Model):
    file = models.FileField(upload_to=database_file_upload_path)


class Email(TimeStampMixin, models.Model):
    thread = models.ForeignKey(Thread, related_name='get_emails', on_delete=models.CASCADE)
    raw_data = JSONField()

    html_content = models.TextField()
    text_content = models.TextField()

    attachments = models.ManyToManyField(Attachment, related_name='get_email')
