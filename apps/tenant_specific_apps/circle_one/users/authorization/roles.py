from rest_framework.permissions import BasePermission, SAFE_METHODS

from apps.tenant_specific_apps.circle_one.users.models import UserProfile
from utils.tenants import is_master_tenant


def user_role(user):
    return hasattr(user, 'get_profile') and \
           user.get_profile and \
           user.get_profile.role


def is_tenant_admin(user):
    return bool(not is_master_tenant() and user_role(user) == UserProfile.ROLE_ADMIN)


class IsTenantAdmin(BasePermission):
    """
    Allows a tenant's admin
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and is_tenant_admin(request.user))


class IsTenantUser(BasePermission):
    """
    Allow only tenant users, disallow in master context
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and not is_master_tenant())


class IsTenantAdminOrReadOnlyIfTenantUser(BasePermission):
    """
    Allows any tenant user to read. Only admin can update
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and is_tenant_admin(request.user)
        )
