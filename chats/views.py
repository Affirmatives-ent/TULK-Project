from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import File, Message, Conversations
from .serializers import MessageSerializer, ConversationSerializer
from django.contrib.auth import get_user_model
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone

User = get_user_model()


class ChatCreateView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        sender = self.request.user
        receiver_id = self.request.data.get('receiver')
        message_content = self.request.data.get('message_content')
        # timestamp = self.request.data.get('timestamp')

        # Ensure that the receiver exists
        receiver = get_object_or_404(User, id=receiver_id)

        # chat = Message.objects.create(
        #     sender=sender, receiver=receiver, message_content=message_content)

        # Check if a conversation already exists between sender and receiver
        conversation = Conversations.objects.filter(
            Q(participant1=sender, participant2=receiver) | Q(
                participant1=receiver, participant2=sender)
        ).first()

        if conversation:
            # Conversation already exists, update the last message
            conversation.last_message = message_content
            conversation.timestamp = timezone.now()
            conversation.save()
        else:
            # Conversation doesn't exist, create a new one
            conversation = Conversations.objects.create(
                participant1=sender, participant2=receiver, last_message=message_content, timestamp=timezone.now())

        serializer.save(sender=sender, receiver=receiver)


class UserChatListView(generics.ListAPIView):
    queryset = Conversations.objects.all()
    serializer_class = ConversationSerializer
    pagination_class = None

    def get_queryset(self):
        # Filter conversations for the current
        user = self.request.user
        return Conversations.objects.filter(Q(participant1=user) | Q(participant2=user))


class ChatConversationView(generics.ListAPIView):
    serializer_class = MessageSerializer
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        receiver_id = self.kwargs.get('receiver_id')
        query = Q(sender=user, receiver=receiver_id) | Q(
            sender=receiver_id, receiver=user)
        return Message.objects.filter(query).order_by('timestamp')
