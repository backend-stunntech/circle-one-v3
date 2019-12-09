from rest_framework import viewsets, mixins

from apps.tenant_specific_apps.circle_one_api.customers.models import Account, Contact, Action, Tag
from apps.tenant_specific_apps.circle_one_api.customers.serializers import AccountSerializer, ContactSerializer, \
    ActionSerializer, TagSerializer
from apps.tenant_specific_apps.circle_one_api.users.authorization.roles import IsTenantUser, \
    OnlyTenantAdminCanDelete


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsTenantUser,)


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (IsTenantUser,)


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = (OnlyTenantAdminCanDelete,)


class ActionViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    permission_classes = (IsTenantUser,)
