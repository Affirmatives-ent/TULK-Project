from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User, Friendship, FriendRequest, Notification
from django.contrib.auth import authenticate
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from posts.models import Like, Post
from article.models import Article
User = get_user_model()


class UserFriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']


class UserProfileSerializer(serializers.ModelSerializer):
    # user_friends = UserFriendsSerializer(
    #     many=True, read_only=True)  # Include this line

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'date_of_birth', 'gender',
                  'email', 'phone_number', 'avatar', 'background_image', 'school', 'marital_status',
                  'bio', 'website', 'location', 'is_staff']

        extra_kwargs = {
            'avatar': {'required': False},
            'background_image': {'required': False},
        }


class TokenExpiredError(serializers.ValidationError):
    default_detail = 'Token has expired.'
    default_code = 407


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get(self.username_field)
        password = attrs.get('password')

        user = None

        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(phone_number=username)
            except User.DoesNotExist:
                pass

        if user is not None:
            if user.check_password(password):
                refresh = self.get_token(user)  # Generate refresh token
                refresh_token = str(refresh)
                access_token = str(refresh.access_token)

                # Serialize the user object using the UserSerializer
                user_serializer = UserProfileSerializer(user)

                return {'access': access_token, 'refresh': refresh_token, 'user': user_serializer.data}

        raise serializers.ValidationError(_('Invalid credentials.'))


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, min_length=settings.MIN_PASSWORD_LENGTH)
    confirm_password = serializers.CharField(
        write_only=True, min_length=settings.MIN_PASSWORD_LENGTH)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number',
                  'date_of_birth', 'gender', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")

        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)

        user = User(**validated_data)
        user.is_active = False
        user.save()

        return user


class VerifyOtpSerializer(serializers.Serializer):
    otp = serializers.CharField(write_only=True, required=True)

    def validate_otp(self, value):
        user = self.context['user']

        if value != user.otp:
            raise serializers.ValidationError("Invalid OTP.")

        if user.otp_expiry and user.otp_expiry < timezone.now():
            raise serializers.ValidationError("OTP has expired.")

        return value

    def validate(self, data):
        user = self.context['user']

        if user.is_active:
            raise serializers.ValidationError("Account is already active.")

        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ForgotPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate_phone_number(self, phone_number):
        # Perform any phone number validation if required
        return phone_number


class VerifyOTPSerializer(serializers.Serializer):
    otp = serializers.CharField()

    def validate_otp(self, otp):
        # Perform any OTP validation if required
        return otp


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, data):
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        # Perform any password validation if required
        if new_password != confirm_password:
            raise serializers.ValidationError("New passwords do not match.")

        return data


class FriendRequestSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    sender_id = serializers.SerializerMethodField()
    sender_avatar = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = '__all__'

    def get_sender_name(self, obj):
        return obj.sender.first_name

    def get_sender_id(self, obj):
        return obj.sender.id

    def get_sender_avatar(self, obj):
        return obj.sender.avatar.url if obj.sender.avatar else None

    def validate(self, data):
        sender = self.context['request'].user
        recipient = data['recipient']

        # Check if a friend request already exists between sender and recipient
        if FriendRequest.objects.filter(sender=sender, recipient=recipient, accepted=False).exists():
            raise serializers.ValidationError(
                "A friend request already exists for this recipient.")

        return data

    def validate_accepted(self, value):
        if self.instance and self.instance.accepted:
            raise serializers.ValidationError(
                "This friend request has already been accepted.")
        return value


# class FriendshipSerializer(serializers.ModelSerializer):
#     user1_data = UserProfileSerializer(source='user1', read_only=True)
#     user2_data = UserProfileSerializer(source='user2', read_only=True)

#     class Meta:
#         model = Friendship
#         fields = ['id', 'user1', 'user2',
#                   'user1_data', 'user2_data', 'created_at']


class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ['user1', 'user2']


# class NotificationSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Notification
#         fields = "__all__"

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"

    def create(self, validated_data):
        # Check if the notification type is 'post_like'
        notification_type = validated_data.get('type')
        if notification_type == 'post_like':
            # Extract the post ID from the request data (if available)
            post_id = self.context.get('post_id')
            if post_id:
                # Add content_type and object_id based on the post ID
                validated_data['content_type'] = ContentType.objects.get_for_model(
                    Like)
                validated_data['object_id'] = post_id

        return super().create(validated_data)


class NotificationCountSerializer(serializers.Serializer):
    count = serializers.IntegerField()


# class UserProfileMediaSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         # Add other relevant fields for UserProfile
#         fields = ('avatar', 'background_image')


# class PostMediaSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = ('files',)  # Add other relevant fields for Post


# class ArticleMediaSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Article
#         fields = ('featured_image', 'files')

class UserMediaSerializer(serializers.Serializer):
    # Define fields that can represent media files from different models
    avatar = serializers.SerializerMethodField()
    background_image = serializers.SerializerMethodField()
    featured_image = serializers.ImageField(read_only=True)
    files = serializers.ListField(
        child=serializers.FileField(), read_only=True)

    def get_avatar(self, obj):
        if hasattr(obj, 'avatar') and obj.avatar:
            return obj.avatar.url
        return None

    def get_background_image(self, obj):
        if hasattr(obj, 'background_image') and obj.background_image:
            return obj.background_image.url
        return None

    def to_representation(self, instance):
        # Create a dictionary that maps model field names to serializer fields
        field_mapping = {
            User: ['avatar', 'background_image'],
            Article: ['featured_image', 'files'],
            Post: ['files'],
            # Add more models and their fields here
        }

        data = {}
        for model, fields in field_mapping.items():
            if isinstance(instance, model):
                for field in fields:
                    if hasattr(instance, field):
                        data[field] = getattr(instance, field)

        return data
