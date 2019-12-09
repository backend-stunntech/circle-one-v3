from django.db import models

from utils.models import TimeStampMixin


class Tag(TimeStampMixin, models.Model):
    name = models.CharField(max_length=256)


class Account(TimeStampMixin, models.Model):
    name = models.CharField(max_length=256)
    tags = models.ManyToManyField(Tag, related_name='get_accounts')


class Contact(TimeStampMixin, models.Model):
    name = models.CharField(max_length=256)
    account = models.ForeignKey(Account, related_name='get_contacts', null=True, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='get_contacts')

    created_by = models.ForeignKey('users.UserProfile', related_name='created_contacts', null=True,
                                   on_delete=models.SET_NULL)


class Action(TimeStampMixin, models.Model):
    REF_ID_START = 1000
    ACTION_EMAIL = 'email'
    ACTION_TICKET = 'ticket'
    ACTION_CHOICES = (
        (ACTION_EMAIL, 'Email'),
        (ACTION_TICKET, 'Ticket'),
    )

    contact = models.ForeignKey(Contact, related_name='get_actions', on_delete=models.CASCADE)
    action_type = models.CharField(choices=ACTION_CHOICES, max_length=10)

    @property
    def ref_id(self):
        return self.REF_ID_START + self.id if self.id else None
