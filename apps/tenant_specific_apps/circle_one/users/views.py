from rest_framework import mixins, viewsets

from apps.tenant_specific_apps.circle_one.users.models import UserProfile
from apps.tenant_specific_apps.circle_one.users.serializers import UserSerializer


class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
