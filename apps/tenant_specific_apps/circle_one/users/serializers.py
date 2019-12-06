from rest_framework import serializers

from apps.tenant_specific_apps.circle_one.users.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'first_name', 'last_name']

    username = serializers.EmailField(source='user.username')
