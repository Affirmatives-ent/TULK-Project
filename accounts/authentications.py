from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

UserModel = get_user_model()


class EmailOrPhoneBackend(BaseBackend):
    def authenticate(self, request, email_or_phone=None, password=None, **kwargs):
        try:
            # try to get user by email
            user = UserModel.objects.get(email=email_or_phone)
        except UserModel.DoesNotExist:
            try:
                # try to get user by phone number
                user = UserModel.objects.get(phone_number=email_or_phone)
            except UserModel.DoesNotExist:
                return None

        if user.check_password(password):
            return user
        else:
            return None

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
