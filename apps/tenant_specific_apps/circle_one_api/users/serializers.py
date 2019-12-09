import random
import string

from django.contrib.auth.models import User
from django.db.transaction import atomic
from rest_framework import serializers

from apps.tenant_specific_apps.circle_one_api.users.models import UserProfile, Department, Group
from utils.tenants import get_current_tenant


class NestedGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        exclude = []


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        exclude = []

    groups = NestedGroupSerializer(many=True, read_only=True)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        exclude = []

    department = DepartmentSerializer()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ['user', 'invited_by']
        extra_kwargs = {
            'require_password_change': {
                'read_only': True
            },
            'avatar': {
                'required': False
            }
        }

    username = serializers.EmailField(source='user.username')
    groups = GroupSerializer(many=True, source='get_groups', read_only=True)

    def validate(self, attrs):
        if 'username' in attrs:
            if self.context['view'].action != 'create':
                attrs.pop('user')
            else:
                _, tenant_domain = attrs['user']['username'].split('@')
                if tenant_domain != get_current_tenant().domain_url:
                    raise serializers.ValidationError({'username': 'Invalid username'})
                try:
                    User.objects.get(username=attrs['user']['username'])
                except User.DoesNotExist:
                    pass
                else:
                    raise serializers.ValidationError({'username': 'User already exits'})
        return attrs

    def create(self, validated_data):
        password = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
        with atomic():
            user = User.objects.create(username=validated_data.pop('user')['username'])
            user.set_password(password)
            user.save()
            profile = user.get_profile
            for key, value in validated_data.items():
                setattr(profile, key, value)
            profile.invited_by = self.context['request'].user.get_profile
            profile.save()
            return profile

    def update(self, instance: 'UserProfile', validated_data):
        if ('role' in validated_data and
                validated_data['role'] != UserProfile.ROLE_ADMIN and
                instance.role == UserProfile.ROLE_ADMIN and
                instance.is_last_admin):
            # do not allow changing last admin to anything else
            raise serializers.ValidationError({'role': 'The only admin\'s role shall not be changed'})


class SignUpVerificationQuerySerializer(serializers.Serializer):
    username = serializers.EmailField()
    verification_token = serializers.CharField()
