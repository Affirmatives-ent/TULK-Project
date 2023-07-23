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
from PIL import Image
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# from django.utils.deconstruct import deconstructible

email_validator = EmailValidator()

phone_regex = RegexValidator(
    regex=r"^\d{10}", message="Phone number must be 13 digits only!"

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
    user_register_at = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(
        upload_to='user_avatar/', blank=True, null=True)
    background_image = models.ImageField(
        upload_to='cover_image/', blank=True, null=True)
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

        # Resize the avatar image
        if self.avatar:
            self.resize_image(self.avatar, (250, 250))

        # Resize the background image
        if self.background_image:
            self.resize_image(self.background_image, (800, 400))

    def resize_image(self, image_field, size):
        image = Image.open(image_field.path)

        # Resize the image while maintaining aspect ratio
        image.thumbnail(size)

        # Save the resized image back to the same field
        image.save(image_field.path)


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
    is_online = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f'{self.user1.first_name} - {self.user2.first_name}'


@receiver([post_save, post_delete], sender=Friendship)
def update_online_status(sender, instance, **kwargs):
    """
    Update online status of users in the friendship and broadcast the changes
    to the OnlineStatusConsumer using channels and WebSockets.
    """
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync
    import json

    # Get the two users involved in the friendship
    user1 = instance.user1
    user2 = instance.user2

    # Determine the online status of each user
    is_user1_online = user1.is_online
    is_user2_online = user2.is_online

    # Broadcast the online status changes to OnlineStatusConsumer
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"online_status_user_{user1.id}",
        {
            "type": "send_online_status",
            "user_id": str(user1.id),
            "is_online": is_user1_online,
        }
    )
    async_to_sync(channel_layer.group_send)(
        f"online_status_user_{user2.id}",
        {
            "type": "send_online_status",
            "user_id": str(user2.id),
            "is_online": is_user2_online,
        }
    )


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_notifications', to_field='id')
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_notifications', to_field='id')
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    viewed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f'{self.sender.first_name} -> {self.recipient.first_name}: {self.message}'
