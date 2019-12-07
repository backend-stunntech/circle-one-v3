from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'apps.tenant_specific_apps.circle_one.users'

    def ready(self):
        # noinspection PyUnresolvedReferences
        from . import signals
