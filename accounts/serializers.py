from rest_framework import serializers
from .models import User, UserProfile


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'first_name', 'last_name', 'gender', 'email', 'phone_number', 'password',
                  'confirm_password')

    def validate(self, data):
        """
        Ensure the password and confirm_password fields match
        """
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("The passwords do not match.")
        return data

    def create(self, validated_data):
        """
        Create a new user instance with the validated data
        """
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number']
        )
        return user


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'email', 'last_name', 'gender', 'phone_number')


class UserProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True)

    class Meta:
        model = UserProfile
        fields = ['url', 'id', 'avatar', 'background_image',
                  'school', 'bio', 'website', 'location', 'user', 'user_id']

        extra_kwargs = {
            'avatar': {'required': False},
            'background_image': {'required': False},
        }

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_id = user_data.pop('id')
        profile = UserProfile.objects.create(user_id=user_id, **validated_data)
        return profile
