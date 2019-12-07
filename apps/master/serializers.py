from uuid import uuid4

from rest_framework import serializers

from apps.master.models import SignUpRequest, Tenant


# class TenantSignupRequestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tenant
#         fields = ['sub_domain', 'admin_username', 'admin_password']
#
#     admin_username = serializers.EmailField(write_only=True)
#     admin_password = serializers.CharField(write_only=True)
#
#     def validate(self, attrs):
#         _, attrs['tenant_domain'] = attrs['admin_username'].split('@')
#         try:
#             Tenant.objects.get(tenant_domain=attrs['tenant_domain'])
#         except Tenant.DoesNotExist:
#             pass
#         else:
#             raise serializers.ValidationError({
#                 'admin_username': f"Tenant domain {attrs['tenant_domain']} already exists."
#             })
#         return attrs
#
#     def create(self, validated_data):
#         tenant = Tenant.create_tenant(tenant_domain=validated_data['tenant_domain'],
#                                       sub_domain=validated_data['sub_domain'])
#         with tenant_context(tenant):
#             admin = User.objects.create(username=validated_data['admin_username'],
#                                         email=validated_data['admin_username'],
#                                         is_active=True,
#                                         is_staff=True)
#             admin.set_password(validated_data['admin_password'])
#             admin.save()
#             admin.get_profile.role = UserProfile.ROLE_ADMIN
#             admin.get_profile.save()
#         return tenant

class TenantSignUpRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignUpRequest
        exclude = ['verification_token', 'tenant_domain', 'created', 'updated', 'id']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate(self, attrs):
        _, tenant_domain = attrs['admin_username'].split('@')
        try:
            Tenant.objects.get(tenant_domain=tenant_domain)
        except Tenant.DoesNotExist:
            attrs['tenant_domain'] = tenant_domain
        else:
            raise serializers.ValidationError({'admin_username': 'Tenant already exist.'})
        return attrs

    def create(self, validated_data):
        validated_data['verification_token'] = uuid4()
        request = super().create(validated_data)
        request.send_verification_email()
        return request
