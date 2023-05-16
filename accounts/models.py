from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.files.storage import default_storage

from django.utils.deconstruct import deconstructible


@deconstructible
class GenerateProfileImagePath(object):
    def __init__(self):
        pass

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        path = f'media/users/{instance.user.id}/images/'
        name = f'profile_image.{ext}'
        return os.path.join(path, name)


user_profile_image_path = GenerateProfileImagePath()


class UserManager(BaseUserManager):
    def create_user(self, email, phone_number, password=None, **kwargs):
        if not email and not phone_number:
            raise ValueError('Users must have an email or phone number')

        if email:
            email = self.normalize_email(email)

        user = self.model(email=email, phone_number=phone_number, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, phone_number, password, **extra_fields)


GENDER_CHOICES = (
    ('MALE', 'Male'),
    ('FEMALE', 'Female'),
)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=6, choices=GENDER_CHOICES, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


MARITAL_STATUS = (
    ('SINGLE', 'Single'),
    ('MARRIED', 'Married'),
    ('DIVORCED', 'Divorced'),
    ('COMPLICATED', 'Complicated'),
    ("I'D RATHER NOT SAY", "I'd Rather Not Say"),
)


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.FileField(
        upload_to='user_profile_image_path', blank=True, null=True)
    background_image = models.FileField(
        upload_to='user_profile_image_path', blank=True, null=True)
    marital_status = models.CharField(
        max_length=20, choices=MARITAL_STATUS, blank=True, null=True)
    school = models.CharField(max_length=100, blank=True, null=True)

    bio = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.user}\'s Profile'
