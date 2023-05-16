from rest_framework import serializers
from .models import User, UserProfile
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'date_of_birth', 'gender',
                  'email', 'phone_number', 'is_active', 'is_staff']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'avatar', 'background_image',
                  'school', 'marital_status', 'bio', 'website', 'location', 'user', 'user_id']

        extra_kwargs = {
            'avatar': {'required': False},
            'background_image': {'required': False},
        }

    # def create(self, validated_data):
    #     user_data = validated_data.pop('user')
    #     user_id = user_data.pop('id')
    #     profile = UserProfile.objects.create(user_id=user_id, **validated_data)
    #     return profile


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number',
                  'date_of_birth', 'gender', 'password']

    def validate(self, data):
        password = data.get('password')
        confirm_password = self.context['request'].data.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")

        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    email_or_phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")
