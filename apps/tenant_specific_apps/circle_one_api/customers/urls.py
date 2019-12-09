from rest_framework.routers import DefaultRouter

from apps.tenant_specific_apps.circle_one_api.customers import viewsets

api_router = DefaultRouter()
api_router.register('tags', viewsets.TagViewSet)
api_router.register('accounts', viewsets.AccountViewSet)
api_router.register('contacts', viewsets.ContactViewSet)
api_router.register('actions', viewsets.ActionViewSet)
urlpatterns = api_router.urls
