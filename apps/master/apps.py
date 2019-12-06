import logging

import django.db
from django.apps import AppConfig
from django.conf import settings

logger = logging.getLogger(__name__)


class MasterConfig(AppConfig):
    name = 'apps.master'

    def ready(self):
        try:
            from django.contrib.sites.models import Site
            from apps.master.models import Tenant
            try:
                Tenant.master()
            except Tenant.DoesNotExist:
                # master tenant needs to exist. create one
                logger.info('Master tenant not found. Creating..')
                Tenant.objects.create(tenant_domain='',
                                      sub_domain='', domain_url=settings.MASTER_DOMAIN,
                                      schema_name=settings.MASTER_SCHEMA_NAME)
                Site.objects.create(name='master tenant', domain=settings.MASTER_DOMAIN)

        except django.db.utils.ProgrammingError:
            # the migrations are not done yet. skip
            logger.info('Migrations are not complete. Skipping master tenant creation..')
