from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.tenant_specific_apps.circle_one.users import views

circle_one_api_router = DefaultRouter()
circle_one_api_router.register('', views.UserViewSet, base_name='users')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(circle_one_api_router.urls))
]
