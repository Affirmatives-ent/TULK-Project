from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import FriendRequest, Friendship
from rest_framework import serializers
from .models import User, Friendship, FriendRequest, Notification
from django.contrib.auth import authenticate
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):

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
    class Meta:
        model = FriendRequest
        fields = '__all__'


class FriendshipSerializer(serializers.ModelSerializer):
    user1_data = UserProfileSerializer(source='user1', read_only=True)
    user2_data = UserProfileSerializer(source='user2', read_only=True)

    class Meta:
        model = Friendship
        fields = ['id', 'user1', 'user2',
                  'user1_data', 'user2_data', 'created_at']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class NotificationCountSerializer(serializers.Serializer):
    count = serializers.IntegerField()
