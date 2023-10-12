from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from django.core.files.storage import default_storage
from django.dispatch import receiver
from django.db.models import Q
from PIL import Image
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.conf import settings
import os
import uuid
from cloudinary_storage.storage import MediaCloudinaryStorage
from django.contrib.contenttypes.models import ContentType


email_validator = EmailValidator()

phone_regex = RegexValidator(
    regex=r"^\d{10}", message="Phone number must be 13 digits only!"
)

GENDER_CHOICES = (
    ('MALE', 'Male'),
    ('FEMALE', 'Female'),
)

MARITAL_STATUS = (
    ('SINGLE', 'Single'),
    ('MARRIED', 'Married'),
    ('DIVORCED', 'Divorced'),
    ('COMPLICATED', 'Complicated'),
    ("I'D RATHER NOT SAY", "I'd Rather Not Say"),
)


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


class User(PermissionsMixin, AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    is_online = models.BooleanField(default=False)
    user_register_at = models.DateTimeField(auto_now_add=True)
    avatar = models.ForeignKey(
        'ProfileMedia',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='users_avatar',
    )

    background_image = models.ForeignKey(
        'ProfileMedia',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='users_background',
    )
    marital_status = models.CharField(
        max_length=20, choices=MARITAL_STATUS, blank=True, null=True)
    school = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.first_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class FriendRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_friend_requests', to_field='id'
    )
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_friend_requests', to_field='id'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f'{self.sender.first_name} -> {self.recipient.first_name}'


class Friendship(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user1 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='friendships1', to_field='id')
    user2 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='friendships2', to_field='id')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f'{self.user1.first_name} - {self.user2.first_name}'


class Notification(models.Model):

    NOTIFICATION_TYPES = [
        ('friend_request', 'Friend Request'),
        ('accept_friend_request', 'Accept Friend Request'),
        ('group_request', 'Group Request'),
        ('group_request_accept', 'Accept Group Request'),
        ('post_comment', 'Post Comment'),
        ('post_like', 'Post Like'),
        ('post_share', 'Post Share'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_notifications', to_field='id')
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_notifications', to_field='id')
    type = models.CharField(
        max_length=30, choices=NOTIFICATION_TYPES, default="friend_request")
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    viewed = models.BooleanField(default=False)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    object_id = models.UUIDField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f'{self.sender.first_name} -> {self.recipient.first_name}: {self.message}'


class ProfileMedia(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="profile_media_user", to_field="id")
    file = models.FileField(upload_to='user_files/',
                            storage=MediaCloudinaryStorage())
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"Media owned by {self.user.first_name}"
