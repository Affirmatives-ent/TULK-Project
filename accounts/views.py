
from rest_framework import generics
from . import serializers, models
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404

from . import serializers
from .models import UserProfile

User = get_user_model()


class UserRegisterationAPIView(GenericAPIView):
    """
    An endpoint for the client to create a new User.
    """

    permission_classes = (AllowAny,)
    serializer_class = serializers.UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(
            token), "access": str(token.access_token)}
        return Response(data, status=status.HTTP_201_CREATED)


class UserLoginAPIView(GenericAPIView):
    """
    An endpoint to authenticate existing users using their email and password.
    """

    permission_classes = (AllowAny,)
    serializer_class = serializers.UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        serializer = serializers.UserSerializer(
            user, context={'request': request})
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(
            token), "access": str(token.access_token)}
        return Response(data, status=status.HTTP_200_OK)


class UserLogoutAPIView(GenericAPIView):
    """
    An endpoint to logout users.
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserAPIView(RetrieveUpdateAPIView):
    """
    Get, Update user information
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        # Retrieve the user profile
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        # Update the user profile
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        # Partial update of the user profile
        return self.partial_update(request, *args, **kwargs)


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    """
    Get, Update user profile
    """

    serializer_class = serializers.UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        user = self.request.user
        profile = get_object_or_404(models.UserProfile, user=user)
        return profile

    def get(self, request, *args, **kwargs):
        # Retrieve the user profile
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        # Update the user profile
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        # Partial update of the user profile
        return self.partial_update(request, *args, **kwargs)
