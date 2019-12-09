from utils.django_admin_customizations.utils import register_model
from apps.tenant_specific_apps.circle_one_api.users.models import UserProfile

register_model((UserProfile,))
