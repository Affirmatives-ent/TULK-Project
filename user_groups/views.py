

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
from posts.models import Post
from articles.models import Article
from accounts.models import Friendship, Notification
from accounts.serializers import UserSerializer
from django.utils import timezone
from django.utils.timezone import make_aware
from django.db.models import Q
import datetime
import random

User = get_user_model


class CreateConversationGroup(generics.CreateAPIView):
    serializer_class = serializers.ConversationGroupSerializer
    permission_classes = [IsAuthenticated]


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
                user=user, message='You have a new group invitation.')
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
        serializer = UserSerializer(friend_list, many=True)
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
