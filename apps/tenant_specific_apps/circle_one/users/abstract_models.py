from django.db import models


class AbstractUserProfile(models.Model):
    class Meta:
        abstract = True

    ROLE_AGENT = 'agent'
    ROLE_MANAGER = 'manager'
    ROLE_ADMIN = 'admin'
    ROLE_CHOICES = (
        (ROLE_AGENT, 'Agent'),
        (ROLE_MANAGER, 'Manager'),
        (ROLE_ADMIN, 'Admin')
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
