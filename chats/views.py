from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import File, Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatCreateView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    parser_classes = (MultiPartParser, FormParser)  # Enable file uploads

    def perform_create(self, serializer):
        sender = self.request.user
        receiver_id = self.request.data.get('receiver')

        # Ensure that the receiver exists
        receiver = get_object_or_404(User, id=receiver_id)

        chat = Message.objects.create(
            sender=sender, receiver=receiver)

        serializer.save(sender=sender, receiver=receiver)


class UserChatList(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        user = self.request.user
        # Retrieve all unique users that the current user has communicated with
        query = Q(sender=user) | Q(receiver=user)
        return Message.objects.filter(query).order_by('sender', '-timestamp').distinct('sender')


class ConversationListView(generics.ListAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def get_queryset(self):
        # Filter conversations for the current user
        user = self.request.user
        return Conversation.objects.filter(participants=user)
