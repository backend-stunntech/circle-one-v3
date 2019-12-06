from rest_framework import viewsets, mixins

from apps.master.serializers import TenantSignupRequestSerializer


class TenantSignupView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = TenantSignupRequestSerializer
