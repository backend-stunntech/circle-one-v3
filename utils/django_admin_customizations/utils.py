from django.contrib import admin
from django.contrib.admin.options import BaseModelAdmin

from apps.tenant_specific_apps.circle_one_api.users.authorization.roles import is_tenant_admin


class ModelPermissionMixin(BaseModelAdmin):
    def is_admin(self, request):
        return is_tenant_admin(request.user)

    def has_module_permission(self, request):
        return self.is_admin(request)

    def has_view_permission(self, request, obj=None):
        return self.is_admin(request)

    def has_change_permission(self, request, obj=None):
        return self.is_admin(request)

    def has_add_permission(self, request):
        return self.is_admin(request)

    def has_delete_permission(self, request, obj=None):
        return self.is_admin(request)


class DefaultModelAdmin(ModelPermissionMixin, admin.ModelAdmin):
    pass


def register_model(model, admin_class=DefaultModelAdmin):
    admin.site.register(model, admin_class)
