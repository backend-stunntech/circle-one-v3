from django.db import models

from utils.models import TimeStampMixin


class Account(TimeStampMixin, models.Model):
    name = models.CharField(max_length=256)


class Contact(TimeStampMixin, models.Model):
    name = models.CharField(max_length=256)
    account = models.ForeignKey(Account, related_name='get_contacts', null=True, on_delete=models.CASCADE)

    created_by = models.ForeignKey('users.UserProfile', related_name='created_contacts', null=True, on_delete=models.SET_NULL)
