from rest_framework import generics

from apps.tenant_specific_apps.circle_one.users.authorization.roles import IsTenantAdmin, IsTenantUser
from apps.tenant_specific_apps.circle_one.users.serializers import UserProfileSerializer


class CurrentUserView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsTenantUser,)
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user.get_profile
