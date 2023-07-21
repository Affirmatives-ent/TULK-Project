from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from django.contrib.auth import authenticate, update_session_auth_hash
from rest_framework import status, generics, mixins, pagination
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from . import serializers, models, utils
from django.contrib.auth import get_user_model
from posts.models import Post
from user_groups.models import ConversationGroup
from articles.models import Article
from django.utils import timezone
from django.utils.timezone import make_aware
from django.db.models import Q
import datetime
import random
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer, TokenExpiredError
from datetime import datetime, timedelta

User = get_user_model()


class WelcomeAPIView(APIView):
    def get(self, request):
        return Response({"message": "Welcome to the TULK Social!"})


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny,]
    serializer_class = serializers.UserRegistrationSerializer
    user_serializer_class = serializers.UserProfileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']

        # Generate a six-digit OTP
        otp = str(random.randint(100000, 999999))
        print(otp)

        # Send the OTP to the user's phone number
        utils.send_otp(phone_number, otp)

        # Create the user object and set it to inactive
        user = serializer.save(is_active=False, otp=otp,
                               otp_expiry=datetime.now() + timedelta(minutes=1))
        print(user.id)

        # Serialize the user object using UserSerializer
        user_serializer = self.user_serializer_class(
            user, context={'request': request})

        # Include the serialized user object in the response
        response_data = {
            "user_id": user.id,
            "user": user_serializer.data,
            "message": "OTP sent successfully"
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class ResendOTPAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')

        try:
            user = User.objects.get(id=user_id)

            # Check if the OTP is expired
            current_time = datetime.datetime.now()
            if user.otp_expiry and current_time > user.otp_expiry:
                # Generate a new OTP and update the user's OTP and OTP expiry
                otp = str(random.randint(100000, 999999))
                user.otp = otp
                user.otp_expiry = datetime.now() + timedelta(minutes=1)
                user.save()

                # Send the new OTP to the user's phone number
                utils.send_otp(user.phone_number, otp)

                return Response({"message": "New OTP sent successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "OTP has not expired yet"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


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


# class UserListAPIView(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = serializers.UserSerializer
#     permission_classes = [IsAdminUser]
#     pagination_class = pagination.PageNumberPagination


# class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = serializers.UserSerializer
#     permission_classes = [IsAdminUser]

    # ... other actions such as create, retrieve, update, partial_update, destroy ...


class UserProfileListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserProfileSerializer
    pagination_class = pagination.PageNumberPagination


class UserProfileDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserProfileSerializer

    def get_object(self):
        user = self.request.user
        return user


class FriendRequestListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.FriendRequest.objects.all()
    serializer_class = serializers.FriendRequestSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = pagination.PageNumberPagination

    def perform_create(self, serializer):
        friend_request = serializer.save(sender=self.request.user)

        # Create a notification for the recipient
        recipient = friend_request.recipient
        notification = models.Notification.objects.create(
            sender=self.request.user,
            recipient=recipient,
            message=f'{self.request.user.username} sent you a friend request.'
        )
        notification_serializer = serializers.NotificationSerializer(
            notification)
        return Response(notification_serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(recipient=user)


class FriendRequestRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FriendRequest.objects.all()
    serializer_class = serializers.FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        friend_request = self.get_object()
        accepted = request.data.get('accepted', False)

        # Update the friend request status
        friend_request.accepted = accepted
        friend_request.save()

        if accepted:
            # Create a friendship if the request is accepted
            models.Friendship.objects.create(
                user1=friend_request.sender, user2=friend_request.recipient)

            # Create a notification for the sender
            notification = models.Notification.objects.create(
                sender=friend_request.recipient,
                recipient=friend_request.sender,
                message=f'{friend_request.recipient.username} accepted your friend request.'
            )
            notification_serializer = serializers.NotificationSerializer(
                notification)
            return Response(notification_serializer.data, status=status.HTTP_200_OK)

        return Response(self.get_serializer(friend_request).data)


class FriendshipListAPIView(generics.ListAPIView):
    queryset = models.Friendship.objects.all()
    serializer_class = serializers.FriendshipSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user1=user) | self.queryset.filter(user2=user)


class FriendshipCreateAPIView(generics.CreateAPIView):
    queryset = models.Friendship.objects.all()
    serializer_class = serializers.FriendshipSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user1 = self.request.user
        user2 = serializer.validated_data['user2']

        # Check if the friendship already exists
        if models.Friendship.objects.filter(user1=user1, user2=user2).exists() or \
           models.Friendship.objects.filter(user1=user2, user2=user1).exists():
            return Response({'detail': 'Friendship already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(user1=user1)


# class FriendSearchAPIView(generics.ListAPIView):
#     serializer_class = serializers.FriendshipSerializer
#     permission_classes = [IsAuthenticated]
#     pagination_class = CustomPagination

#     def get_queryset(self):
#         search_query = self.request.query_params.get('search')
#         admin = self.request.user

#         # Filter the friends based on the search query
#         friends = models.Friendship.objects.filter(
#             Q(user1=admin, user2__first_name__icontains=search_query) |
#             Q(user1=admin, user2__last_name__icontains=search_query)
#         )

#         return friends


class NotificationListAPIView(generics.ListAPIView):
    queryset = models.Notification.objects.all()
    serializer_class = serializers.NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(recipient=user)


class NotificationUpdateAPIView(generics.UpdateAPIView):
    queryset = models.Notification.objects.all()
    serializer_class = serializers.NotificationSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        notification = self.get_object()
        notification.read = True
        notification.save()
        return Response(self.get_serializer(notification).data, status=status.HTTP_200_OK)


class NotificationCountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        notification_count = models.Notification.objects.filter(
            recipient=user, read=False).count()
        serializer = serializers.NotificationCountSerializer(
            {'count': notification_count})
        return Response(serializer.data, status=status.HTTP_200_OK)


class SearchAPIView(generics.ListAPIView):
    serializer_class = serializers.SearchSerializer
    permission_classes = [AllowAny]
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        search_query = self.request.query_params.get('search')

        # Perform the search query across multiple models and fields
        results = []

        # Search for users by username, first name, or last name
        user_results = User.objects.filter(
            Q(phone_number__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
        results.extend(user_results)

        # Search for groups by name or category
        group_results = ConversationGroup.objects.filter(
            Q(name__icontains=search_query) |
            Q(category__icontains=search_query)
        )
        results.extend(group_results)

        # Search for posts or articles by title or category
        post_results = Post.objects.filter(
            Q(title__icontains=search_query) |
            Q(category__icontains=search_query)
        )
        results.extend(post_results)

        # Search for articles by title or category
        article_results = Article.objects.filter(
            Q(title__icontains=search_query) |
            Q(category__icontains=search_query)
        )
        results.extend(article_results)

        return results
