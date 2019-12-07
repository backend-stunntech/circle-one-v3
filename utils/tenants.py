from django.conf import settings
from django.db import connection


def get_current_tenant():
    return connection.tenant


def get_current_schema_name():
    return connection.tenant.schema_name


def is_master_tenant():
    return get_current_schema_name() == settings.MASTER_SCHEMA_NAME
