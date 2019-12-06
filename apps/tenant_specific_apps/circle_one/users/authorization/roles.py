from apps.tenant_specific_apps.circle_one.users.models import UserProfile
from CircleOneV3.utils import is_master_tenant


def user_role(user):
    return hasattr(user, 'get_profile') and \
           user.get_profile and \
           user.get_profile.role


def is_saas_admin(user):
    return  not is_master_tenant() and user_role(user) == UserProfile.ROLE_ADMIN
