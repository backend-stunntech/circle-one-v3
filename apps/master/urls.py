from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.master.views import TenantSignupView

api_router = DefaultRouter()
api_router.register('', TenantSignupView, 'signup')

urlpatterns = [
    path('api/v1/', include(api_router.urls)),
    path('admin/', admin.site.urls),
]
