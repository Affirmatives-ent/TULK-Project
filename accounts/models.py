from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.models import AbstractUser
import os
import uuid
from django.conf import settings
from django.core.validators import RegexValidator
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.files.storage import default_storage

from django.utils.deconstruct import deconstructible

email_validator = EmailValidator()

phone_regex = RegexValidator(
    regex=r"^\d{10}", message="Phone number must be 13 digits only!"

)


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
    def create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        if not phone_number and not email:
            raise ValueError(
                "Either the Phone Number or Email field must be set.")

        # Normalize the email and phone number
        email = self.normalize_email(email) if email else None
        phone_number = self.normalize_phone_number(
            phone_number) if phone_number else None

        # Create the user instance
        user = self.model(
            email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email=email, phone_number=phone_number, password=password, **extra_fields)

    def normalize_phone_number(self, phone_number):
        """
        Normalize the phone number by removing non-digit characters.
        """
        return ''.join(filter(str.isdigit, str(phone_number)))


GENDER_CHOICES = (
    ('MALE', 'Male'),
    ('FEMALE', 'Female'),
)


class User(PermissionsMixin, AbstractBaseUser):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=6, choices=GENDER_CHOICES, blank=True, null=True)
    email = models.EmailField(
        unique=True, max_length=50, validators=[email_validator])
    phone_number = models.CharField(
        max_length=30, unique=True, blank=False, null=False, validators=[phone_regex])
    otp = models.CharField(max_length=6, db_index=True)
    reset_password_otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expiry = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    user_register_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.first_name


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
    avatar = models.ImageField(
        upload_to='user_profile_image_path', blank=True, null=True)
    background_image = models.ImageField(
        upload_to='user_profile_image_path', blank=True, null=True)
    marital_status = models.CharField(
        max_length=20, choices=MARITAL_STATUS, blank=True, null=True)
    school = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.user}\'s Profile'


class FriendRequest(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_friend_requests')
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_friend_requests')
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender.username} -> {self.recipient.username}'


class Friendship(models.Model):
    user1 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='friendships1')
    user2 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='friendships2')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user1.username} - {self.user2.username}'


class Notification(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_notifications')
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_notifications')
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    viewed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender.username} -> {self.recipient.username}: {self.message}'
