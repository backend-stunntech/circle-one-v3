from django.urls import include, path
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import obtain_auth_token

# built-in token generation api for login:
obtain_auth_token = swagger_auto_schema(method='post',
                                        operation_summary='Request token for user authentication',
                                        request_body=AuthTokenSerializer)(obtain_auth_token)

urlpatterns = [
    path('auth/', obtain_auth_token, name='auth'),
    path('users/', include('apps.tenant_specific_apps.circle_one_api.users.urls')),
    path('customers/', include('apps.tenant_specific_apps.circle_one_api.customers.urls')),
    path('emails/', include('apps.tenant_specific_apps.circle_one_api.emails.urls')),
]
