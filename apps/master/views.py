from django.conf import settings
from django.http import Http404, HttpResponseRedirect
from rest_framework import viewsets, mixins, views

from apps.master.models import SignUpRequest
from apps.master.serializers import TenantSignUpRequestSerializer


class TenantSignupView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = TenantSignUpRequestSerializer


class SignUpVerification(views.APIView):
    def get(self, *args, **kwargs):
        verification_token = self.request.query_params.get('verification_token')
        admin_username = self.request.query_params.get('username')
        if verification_token and admin_username:
            tenant = SignUpRequest.verify(verification_token, admin_username)
            redirect_url = f"https://{tenant.sub_domain}.{settings.FRONTEND_MASTER_DOMAIN}/"
            return HttpResponseRedirect(redirect_url)
        else:
            raise Http404
