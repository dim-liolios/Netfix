from django.contrib.auth.backends import BaseBackend
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            User = get_user_model()
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
