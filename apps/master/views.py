import logging

from django.http import Http404, HttpResponseRedirect, HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import views, generics

from apps.master.models import SignUpRequest
from apps.master.serializers import TenantSignUpRequestSerializer
from apps.tenant_specific_apps.circle_one_api.users.serializers import SignUpVerificationQuerySerializer

logger = logging.getLogger(__file__)

class TenantSignupView(generics.CreateAPIView):
    serializer_class = TenantSignUpRequestSerializer


class SignUpVerification(views.APIView):
    @swagger_auto_schema(query_serializer=SignUpVerificationQuerySerializer)
    def get(self, *args, **kwargs):
        verification_token = self.request.query_params.get('verification_token')
        admin_username = self.request.query_params.get('username')
        if verification_token and admin_username:
            tenant = SignUpRequest.verify(verification_token, admin_username)
            redirect_url = f"{tenant.login_link}"
            return HttpResponseRedirect(redirect_url)
        else:
            raise Http404




class AwsSnsWebHook(views.APIView):
    def post(self):
        logger.info(self.request)
        return HttpResponse('Success')
