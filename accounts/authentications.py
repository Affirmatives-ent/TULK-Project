# from django.contrib.auth import get_user_model
# from django.contrib.auth.backends import ModelBackend

# UserModel = get_user_model()

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return

        # Check if the username is a valid phone number
        if username.isdigit():
            try:
                user = User.objects.get(phone_number=username)
            except User.DoesNotExist:
                return None
        else:
            # Check if the username is a valid email address
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None

        # Verify the password
        if user.check_password(password):
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


# class EmailOrPhoneBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         try:
#             user = UserModel.objects.get(email=username)
#         except UserModel.DoesNotExist:
#             try:
#                 user = UserModel.objects.get(phone_number=username)
#             except UserModel.DoesNotExist:
#                 return None

#         if user.check_password(password):
#             return user

#     def get_user(self, user_id):
#         try:
#             return UserModel.objects.get(pk=user_id)
#         except UserModel.DoesNotExist:
#             return None
