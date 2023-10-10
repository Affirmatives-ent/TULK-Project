from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Chat, File, Message
from .serializers import MessageSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatListView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    parser_classes = (MultiPartParser, FormParser)  # Enable file uploads

    def get_queryset(self):
        user = self.request.user
        print(user)
        print(user)
        return Message.objects.filter(Q(sender=user) | Q(receiver=user))

    def perform_create(self, serializer):
        sender = self.request.user
        receiver_id = self.request.data.get('receiver')

        # Ensure that the receiver exists
        receiver = get_object_or_404(User, id=receiver_id)

        chat, _ = Message.objects.get_or_create(
            sender=sender, receiver=receiver)

        serializer.save(sender=sender, receiver=receiver)


class ChatDetailView(generics.RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class ChatConversationListView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    parser_classes = (MultiPartParser, FormParser)  # Enable file uploads

    def get_queryset(self):
        user = self.request.user
        receiver_id = self.kwargs.get('receiver_id')
        return Message.objects.filter(
            Q(sender=user, receiver=receiver_id) | Q(
                sender=receiver_id, receiver=user)
        )

    def perform_create(self, serializer):
        sender = self.request.user
        receiver_id = self.kwargs.get('receiver_id')

        # Ensure that the receiver exists
        receiver = get_object_or_404(User, id=receiver_id)

        message_content = self.request.data.get('message', '')
        files = self.request.data.getlist('files')  # Handle multiple files

        chat, _ = Message.objects.get_or_create(
            sender=sender, receiver=receiver)

        message = chat.get_or_create_message(
            sender, receiver, message_content, files)

        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
