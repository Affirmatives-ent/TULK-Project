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
from posts.models import Post, File
from posts.serializers import PostSerializer, FileSerializer
from user_groups.models import ConversationGroup
from user_groups.serializers import ConversationGroupSerializer
from article.models import Article
from article.serializers import ArticleSerializer
from django.utils import timezone
from django.utils.timezone import make_aware
from rest_framework import exceptions
from django.db.models import Q
import datetime
import random
from django.contrib.contenttypes.models import ContentType
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer, TokenExpiredError
from datetime import datetime, timedelta
from rest_framework.pagination import PageNumberPagination

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

        phone = user.phone_number

        if user is None:
            return Response({"message": "No active user found with the provided phone number."}, status=status.HTTP_400_BAD_REQUEST)

        # Generate a six-digit OTP
        otp = str(random.randint(100000, 999999))
        print(otp)

        utils.send_otp(phone, otp)
        print(phone)

        # Save the OTP in the user's model
        user.reset_password_otp = otp
        user.save()

        return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)


class VerifyPasswordOTPAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = serializers.VerifyPasswordOTPSerializer(data=request.data)
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
        otp = request.session.get('verified_otp')
        if otp is None:
            return Response({"message": "OTP verification required."}, status=status.HTTP_400_BAD_REQUEST)

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


class UserProfileListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserProfileSerializer
    pagination_class = None


class UserProfileDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user_id = self.kwargs.get('pk')
        user = get_object_or_404(User, pk=user_id)
        return user

    def update(self, request, *args, **kwargs):
        user_id = self.kwargs.get('pk')
        user = get_object_or_404(User, pk=user_id)

        if user != request.user:
            return Response(
                {'detail': 'You do not have permission to update this user.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)

        print("Before processing friends")

        # Fetch and add the list of friends to the serialized data
        friendships1 = models.Friendship.objects.filter(user1=user)
        friendships2 = models.Friendship.objects.filter(user2=user)

        friends = set(friendship.user2 for friendship in friendships1)
        friends |= set(friendship.user1 for friendship in friendships2)

        print("After processing friends")
        # Ensure friends are unique and exclude the user themselves
        print(friends)
        friends.discard(user)

        user_friends_data = serializers.UserFriendsSerializer(
            friends, many=True).data
        print(user_friends_data)
        serializer.data['user_friends'] = user_friends_data
        # print(serializer.data)

        return Response(serializer.data)


class FriendRequestListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.FriendRequest.objects.all()
    serializer_class = serializers.FriendRequestSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def perform_create(self, serializer):
        sender = self.request.user
        recipient = serializer.validated_data['recipient']

        # Check if a friend request already exists between sender and recipient
        if models.FriendRequest.objects.filter(Q(sender=sender, recipient=recipient, accepted=False) | Q(sender=recipient, recipient=sender, accepted=False)).exists():
            raise exceptions.ValidationError(
                "A friend request already exists for this recipient.")

        # Check if the users are already friends
        if models.Friendship.objects.filter(
                (Q(user1=sender, user2=recipient) |
                 Q(user1=recipient, user2=sender))
        ).exists():
            raise exceptions.ValidationError(
                "You are already friends with this user.")

        friend_request = serializer.save(sender=sender)

        request_id = models.FriendRequest.objects.filter(
            sender=sender, recipient=recipient, accepted=False).get().id

        # Create a notification for the recipient
        notification = models.Notification.objects.create(
            sender=sender,
            recipient=recipient,
            message=f'{sender.first_name} sent you a friend request.',
            type='friend_request',
            content_type=ContentType.objects.get_for_model(
                models.FriendRequest),
            object_id=request_id
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
            friendship = models.Friendship.objects.create(
                user1=friend_request.sender, user2=friend_request.recipient
            )
            notification = models.Notification.objects.create(
                sender=friend_request.recipient,
                recipient=friend_request.sender,
                message=f'{friend_request.recipient.first_name} accepted your friend request.',
                type=friend_request.type.accept_friend_request
            )
            notification_serializer = serializers.NotificationSerializer(
                notification)
            return Response(notification_serializer.data, status=status.HTTP_200_OK)

        return Response(self.get_serializer(friend_request).data)


class FriendsListAPIView(generics.ListAPIView):
    serializer_class = serializers.UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        friendships = models.Friendship.objects.filter(
            Q(user1=user_id) | Q(user2=user_id)
        )
        print(friendships)
        friend_ids = []
        for friendship in friendships:
            if user_id == friendship.user1.id:
                friend_ids.append(friendship.user2.id)
            elif user_id == friendship.user2.id:
                friend_ids.append(friendship.user1.id)

        print(friend_ids)

        friends_data = models.User.objects.filter(id__in=friend_ids)
        print(friends_data)
        return friends_data

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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

    # def get(self, request, format=None):
    #     user = request.user

    def update(self, request, *args, **kwargs):
        notification = self.get_object()
        notification.viewed = True
        notification.save()
        if notification.type == 'friend_request':
            sender = notification.sender
            user = notification.recipient
            models.Friendship.objects.create(user1=sender, user2=user)

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


class UserNotificationListView(generics.ListAPIView):
    serializer_class = serializers.NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return models.Notification.objects.filter(recipient=user)


class SearchAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        results = []

        if 'search' in self.request.GET:
            search_query = self.request.query_params.get('search')
            model = self.request.query_params.get(
                'model')  # Get the 'model' query parameter

            if model == 'users':
                user_results = User.objects.filter(
                    Q(phone_number__icontains=search_query) |
                    Q(first_name__icontains=search_query) |
                    Q(last_name__icontains=search_query)
                )
                user_serializer = serializers.UserProfileSerializer(
                    user_results, many=True)
                results.extend(user_serializer.data)

            elif model == 'posts':
                posts_results = Post.objects.filter(
                    Q(author__first_name__icontains=search_query) | Q(
                        content__icontains=search_query)
                )
                post_serializer = PostSerializer(posts_results, many=True)
                results.extend(post_serializer.data)

            elif model == 'groups':
                group_results = ConversationGroup.objects.filter(
                    Q(name__icontains=search_query) |
                    Q(category__icontains=search_query)
                )
                group_serializer = ConversationGroupSerializer(
                    group_results, many=True)
                results.extend(group_serializer.data)

            elif model == 'articles':
                articles_results = Article.objects.filter(
                    Q(title__icontains=search_query) |
                    Q(category__icontains=search_query) |
                    Q(author__first_name__icontains=search_query)
                )
                article_serializer = ArticleSerializer(
                    articles_results, many=True)
                results.extend(article_serializer.data)

        return Response({"data": results})


class UserMediaFilesView(generics.ListAPIView):
    serializer_class = FileSerializer  # Define the serializer class
    pagination_class = None

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        # Retrieve the user based on user_id
        user = get_object_or_404(User, id=user_id)

        # Query Files objects associated with the user
        post_media_files = File.objects.filter(post__author=user)

        return post_media_files
