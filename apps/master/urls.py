from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from apps.master.views import TenantSignupView, SignUpVerification, AwsSnsWebHook

urlpatterns = [
    path('api/v1/signup', TenantSignupView.as_view()),
    path('api/v1/signup-verification/', SignUpVerification.as_view(), name='signup-verification'),
    path('admin/', admin.site.urls),
    path('sns-web-hook/', AwsSnsWebHook.as_view(), name='sns-web-hook')
]

# Swagger(OpenApi) documentation urls:
schema_view = get_schema_view(
    openapi.Info(
        title="Circle One API",
        default_version='v1',
        # description="Test description",
        # terms_of_service="https://www.google.com/policies/terms/",
        # contact=openapi.Contact(email="contact@snippets.local"),
        # license=openapi.License(name="BSD License"),
    ),
    patterns=urlpatterns,
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    # urls for api documentation
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
