

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import action
from django.contrib.auth import authenticate, update_session_auth_hash
from rest_framework import status, generics, mixins
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from . import serializers, models
from .permissions import IsGroupAdmin
from django.contrib.auth import get_user_model
from article.models import Article
from accounts.models import Friendship, Notification
from accounts.serializers import UserProfileSerializer
from django.utils import timezone
from django.utils.timezone import make_aware
from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
import datetime
import random
from .models import ConversationGroup, Comment, Like, GroupMedia, GroupPost
from .serializers import GroupPostSerializer, CommentSerializer, LikeSerializer, GroupMediaSerializer

User = get_user_model


class CreateConversationGroup(generics.CreateAPIView):
    serializer_class = serializers.ConversationGroupSerializer
    permission_classes = [IsAuthenticated]


class ListConversationGroups(generics.ListAPIView):
    queryset = ConversationGroup.objects.all()
    serializer_class = serializers.ConversationGroupSerializer
    permission_classes = [IsAuthenticated]


class ConversationGroupDetail(generics.RetrieveUpdateAPIView):
    queryset = ConversationGroup.objects.all()
    serializer_class = serializers.ConversationGroupSerializer
    permission_classes = [IsAuthenticated]


class ConversationGroupDetailUpdate(generics.RetrieveUpdateAPIView):
    queryset = ConversationGroup.objects.all()
    serializer_class = serializers.ConversationGroupUpdateSerializer
    permission_classes = [IsGroupAdmin]


class InviteUserToGroup(APIView):
    permission_classes = [IsAuthenticated, IsGroupAdmin]

    def post(self, request, group_id):
        try:
            group = models.ConversationGroup.objects.get(id=group_id)
            user_id = request.data.get('user_id')
            user = User.objects.get(id=user_id)

            # Check if the user is already a member of the group
            if user in group.members.all():
                return Response({'detail': 'User is already a member of the group.'}, status=400)

            # Check if the group admin and the user are friends
            friendship = Friendship.objects.filter(
                (Q(user1=request.user) & Q(user2=user)) | (
                    Q(user1=user) & Q(user2=request.user))
            ).first()

            if not friendship:
                return Response({'detail': 'User is not on your friend list.'}, status=400)

            # Add the user to the group's pending members
            group.members.add(user)
            group.save()

            # Create a notification for the invited user
            notification = Notification(
                sender=group.admin,
                recipient=user,
                type=Notification.NOTIFICATION_TYPES.group_request,
                message='You have a new group invitation.',
            )
            notification.save()

            serializer = serializers.ConversationGroupSerializer(group)
            return Response(serializer.data)
        except models.ConversationGroup.DoesNotExist:
            return Response(status=404)
        except User.DoesNotExist:
            return Response(status=404)


class FriendSearch(APIView):
    permission_classes = [IsAuthenticated, IsGroupAdmin]

    def get(self, request):
        query = request.query_params.get('query', '')
        friends = Friendship.objects.filter(
            Q(user1=request.user) | Q(user2=request.user),
            Q(user1__username__icontains=query) | Q(
                user2__username__icontains=query)
        )
        friend_list = []
        for friend in friends:
            friend_user = friend.user1 if friend.user1 != request.user else friend.user2
            friend_list.append(friend_user)

        # Replace with your User serializer
        serializer = UserProfileSerializer(friend_list, many=True)
        return Response(serializer.data)


class AcceptOrRejectInvitation(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, group_id):
        try:
            group = models.ConversationGroup.objects.get(id=group_id)
            user = request.user
            invitation_status = request.data.get('invitation_status')

            # Check if the user is a pending member of the group
            if user not in group.members.all() or group.invitation_status != 'pending':
                return Response({'detail': 'Invalid invitation.'}, status=400)

            # Update the invitation status based on the user's response
            if invitation_status == 'accept':
                group.members.remove(user)
                group.members.add(user)
                group.invitation_status = 'accepted'
                group.save()

                # Create a notification for the group owner
                notification = Notification(
                    user=group.owner, message=f'{user.username} accepted the group invitation.')
                notification.save()
            elif invitation_status == 'reject':
                group.members.remove(user)
                group.invitation_status = 'rejected'
                group.save()

                # Create a notification for the group owner
                notification = Notification(
                    user=group.owner, message=f'{user.username} rejected the group invitation.')
                notification.save()
            else:
                return Response({'detail': 'Invalid invitation status.'}, status=400)

            serializer = serializers.ConversationGroupSerializer(group)
            return Response(serializer.data)
        except models.ConversationGroup.DoesNotExist:
            return Response(status=404)


class UserGroupsAPIView(generics.ListAPIView):
    serializer_class = serializers.ConversationGroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ConversationGroup.objects.filter(members=user) | ConversationGroup.objects.filter(admin=user)


class GroupPostListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = PageNumberPagination
    page_size = 10

    def get(self, request, group_id, format=None):  # Extract the group_id from the URL
        # Fetch posts associated with the specific group
        posts = GroupPost.objects.filter(group_id=group_id)

        print(f'This is the post object: {posts}')

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(posts, request)
        serializer = GroupPostSerializer(result_page, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, group_id, format=None):
        serializer = GroupPostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save()

            # Process and save multiple files
            files_data = request.FILES.getlist('media')
            for file_data in files_data:
                file_instance = GroupMedia(file=file_data)
                file_instance.save()
                post.files.add(file_instance)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GroupPost.objects.all()
    serializer_class = GroupPostSerializer
    permission_classes = [IsAuthenticated]


class UserPostsAPIView(APIView):
    def get(self, request, group_id, format=None):
        try:
            posts = GroupPost.objects.filter(
                group__id=group_id).order_by('-created_at')
            serializer = GroupPostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)


class CommentListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        # Get the post ID from the URL parameter
        post_id = self.kwargs.get('post_id')
        # Get the post object based on the post ID
        post = get_object_or_404(GroupPost, id=post_id)
        # Filter the comments queryset based on the post object
        queryset = Comment.objects.filter(post=post)
        return queryset


class LikeToggleAPIView(APIView):
    def post(self, request, post_id, format=None):
        user = request.user

        try:
            post = GroupPost.objects.get(id=post_id)
        except GroupPost.DoesNotExist:
            return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user already liked the post
        try:
            like = Like.objects.get(user=user, post=post)
            # If the like already exists, remove it
            like.delete()
            return Response({'detail': 'Like removed successfully.'}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            # If the like does not exist, create it
            like = Like.objects.create(user=user, post=post)
            return Response({'detail': 'Like added successfully.'}, status=status.HTTP_201_CREATED)


class LikeListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Like.objects.filter(post_id=post_id)
