from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import File, Message, Conversations
from .serializers import MessageSerializer, ConversationSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatCreateView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    parser_classes = (MultiPartParser, FormParser)  # Enable file uploads

    def perform_create(self, serializer):
        sender = self.request.user
        receiver_id = self.request.data.get('receiver')
        message_content = self.request.data.get('message_content')

        # Ensure that the receiver exists
        receiver = get_object_or_404(User, id=receiver_id)

        chat = Message.objects.create(
            sender=sender, receiver=receiver)

        conversation, created = Conversations.objects.get_or_create(
            participant1=sender, participant2=receiver, last_message=message_content)

        if created:
            conversation.last_message = message_content
            conversation.save()

        # # Update the last message in the conversation
        # conversation.last_message
        # conversation.save()

        # last_message = Message.objects.filter(
        #     sender=sender, receiver=receiver).order_by('-timestamp').first()
        # conversation = Conversation.objects.create(
        #     participant1=sender, participant2=receiver, last_message=last_message)

        serializer.save(sender=sender, receiver=receiver)


# class UserChatList(generics.ListAPIView):
#     serializer_class = MessageSerializer

#     def get_queryset(self):
#         user = self.request.user
#         # Retrieve all unique users that the current user has communicated with
#         query = Q(sender=user) | Q(receiver=user)
#         return Message.objects.filter(query).order_by('sender', '-timestamp').distinct('sender')


class UserChatListView(generics.ListAPIView):
    queryset = Conversations.objects.all()
    serializer_class = ConversationSerializer

    def get_queryset(self):
        # Filter conversations for the current user
        user = self.request.user
        return Conversations.objects.filter(Q(participant1=user) | Q(participant2=user))


class ChatConversationView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        user = self.request.user
        receiver_id = self.kwargs.get('receiver_id')
        query = Q(sender=user, receiver=receiver_id) | Q(
            sender=receiver_id, receiver=user)
        return Message.objects.filter(query).order_by('timestamp')
