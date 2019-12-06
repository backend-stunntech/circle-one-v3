from django.contrib.auth import backends, get_user_model
from django.db.models import Q


class AuthenticationBackend(backends.ModelBackend):
    """
    Custom authentication Backend for login using email as user_id field.
    """

    def authenticate(self, request, email=None, username=None, password=None, **kwargs):
        usermodel = get_user_model()
        try:
            user = usermodel.objects.get(
                Q(username__iexact=email) |
                Q(email__iexact=email) |
                Q(username__iexact=username) |
                Q(email__iexact=username)
            )

            if user.check_password(password):
                return user
        except usermodel.DoesNotExist:
            usermodel().set_password(password)
