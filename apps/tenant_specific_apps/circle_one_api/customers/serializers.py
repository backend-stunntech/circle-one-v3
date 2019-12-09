from rest_framework import serializers

from apps.tenant_specific_apps.circle_one_api.customers.models import Account, Contact, Action, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        exclude = []


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = []

    tags = TagSerializer(many=True)


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        exclude = ['created_by']

    account = AccountSerializer()
    tags = TagSerializer(many=True)


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        exclude = []

    contact = ContactSerializer()
