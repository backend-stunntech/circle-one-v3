from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.tenant_specific_apps.circle_one_api.users import views
from apps.tenant_specific_apps.circle_one_api.users.viewsets import UserProfileViewSet, GroupViewSet, DepartmentViewSet

api_router = DefaultRouter()
api_router.register('', UserProfileViewSet)
api_router.register('groups', GroupViewSet)
api_router.register('departments', DepartmentViewSet)

urlpatterns = api_router.urls + [
    path('me', views.CurrentUserView.as_view()),
]
