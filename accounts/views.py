from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from django.contrib.auth import authenticate, update_session_auth_hash
from rest_framework import status, generics, mixins
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from . import serializers, models, utils
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.timezone import make_aware
import datetime
import random
from rest_framework.permissions import AllowAny

User = get_user_model()


class WelcomeAPIView(APIView):
    def get(self, request):
        return Response({"message": "Welcome to the TULK Social!"})


class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny,]
    serializer_class = serializers.UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']

        # Generate a six-digit OTP
        otp = str(random.randint(100000, 999999))
        print(otp)

        # Send the OTP to the user's phone number (implement your send_otp function)
        utils.send_otp(phone_number, otp)

        # Create the user object and set it to inactive
        user = serializer.save(is_active=False, otp=otp)
        print(user.id)

        # Return the user object along with other data in the response
        response_data = {
            "user_id": user.id,
            "user": serializer.data,
            "message": "OTP sent successfully"
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class VerifyOTPAPIView(generics.GenericAPIView, mixins.UpdateModelMixin):
    queryset = User.objects.filter(is_active=False)
    serializer_class = serializers.VerifyOtpSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        otp = request.data.get('otp')

        try:
            user = self.get_object()
        except User.DoesNotExist:
            return Response({"message": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

        if user.otp != otp:
            return Response({"message": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()
        return Response({"user_id": user.id, "message": "OTP verified and account created successfully."})


class UserLogoutAPIView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "No refresh token provided."}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = serializers.ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']

        # Check if the old password is correct
        if not user.check_password(old_password):
            return Response({"message": "Invalid old password."}, status=status.HTTP_400_BAD_REQUEST)

        # Update the user's password
        user.set_password(new_password)
        user.save()

        # Update the session authentication hash
        update_session_auth_hash(request, user)

        return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)


class ForgotPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = serializers.ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']

        user = User.objects.filter(
            phone_number=phone_number, is_active=True).first()

        if user is None:
            return Response({"message": "No active user found with the provided phone number."}, status=status.HTTP_400_BAD_REQUEST)

        # Generate a six-digit OTP
        otp = str(random.randint(100000, 999999))
        print(otp)

        # Send the OTP to the user's phone number (implement your send_otp function)
        utils.send_otp(phone_number, otp)

        # Save the OTP in the user's model
        user.reset_password_otp = otp
        user.save()

        return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)


class VerifyPasswordOTPAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = serializers.VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp = serializer.validated_data['otp']

        # Find the user with the provided OTP
        user = User.objects.filter(
            reset_password_otp=otp, is_active=True).first()

        if user is None:
            return Response({"message": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

        # Save the verified OTP in the session
        request.session['verified_otp'] = otp

        return Response({"message": "OTP verified successfully."}, status=status.HTTP_200_OK)


class ResetPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = serializers.ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp = request.session.get('verified_otp')
        new_password = serializer.validated_data['new_password']
        confirm_password = serializer.validated_data['confirm_password']

        # Find the user with the verified OTP
        user = User.objects.filter(
            reset_password_otp=otp, is_active=True).first()

        if user is None:
            return Response({"message": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the new passwords match
        if new_password != confirm_password:
            return Response({"message": "New passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        # Update the user's password
        user.set_password(new_password)
        user.reset_password_otp = None
        user.save()

        # Clear the verified OTP from the session
        del request.session['verified_otp']

        return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAdminUser]


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAdminUser]

    # ... other actions such as create, retrieve, update, partial_update, destroy ...


class UserProfileListAPIView(generics.ListAPIView):
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserProfileSerializer


class UserProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
