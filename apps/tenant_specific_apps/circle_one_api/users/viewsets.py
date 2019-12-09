from rest_framework import viewsets, pagination
from rest_framework.exceptions import PermissionDenied

from apps.tenant_specific_apps.circle_one_api.users.authorization.roles import IsTenantAdmin, \
    IsTenantAdminOrReadOnlyIfTenantUser
from apps.tenant_specific_apps.circle_one_api.users.models import UserProfile, Department, Group
from apps.tenant_specific_apps.circle_one_api.users.serializers import UserProfileSerializer, DepartmentSerializer, \
    GroupSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    pagination_class = pagination.PageNumberPagination

    # TODO: clarify user api permissions
    permission_classes = (IsTenantAdmin,)

    def perform_destroy(self, instance: 'UserProfile'):
        # the only admin shall not be deleted
        if instance.is_last_admin:
            raise PermissionDenied('The only admin shall not be deleted')

        # delete the user instead of the profile
        instance.user.delete()


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = (IsTenantAdminOrReadOnlyIfTenantUser,)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = (IsTenantAdminOrReadOnlyIfTenantUser,)
