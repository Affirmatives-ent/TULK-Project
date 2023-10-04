from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Chat, File
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .serializers import ChatSerializer, FileSerializer
User = get_user_model()


class ChatListView(generics.ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    parser_classes = (MultiPartParser, FormParser)  # Enable file uploads

    def get_queryset(self):
        user = self.request.user
        return Chat.objects.filter(Q(sender=user) | Q(receiver=user))


class ChatDetailView(generics.RetrieveAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


class ChatConversationListView(generics.ListCreateAPIView):
    serializer_class = ChatSerializer
    parser_classes = (MultiPartParser, FormParser)  # Enable file uploads

    def get_queryset(self):
        user = self.request.user
        receiver_id = self.kwargs.get('receiver_id')
        result = Chat.objects.filter(Q(sender=user, receiver=receiver_id) | Q(
            sender=receiver_id, receiver=user))

        return result

    def perform_create(self, serializer):
        sender = self.request.user

        receiver_id = self.kwargs.get('receiver_id')

        # Ensure that the receiver exists
        receiver = get_object_or_404(User, id=receiver_id)

        message = self.request.data.get('message', '')
        files = self.request.data.getlist('files')  # Handle multiple files

    # Create a chat message with the encrypted message

        # Check if a conversation between these two users already exists
        chat_message = Chat.objects.filter(
            Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender)).first()

        if chat_message is None:
            # If no conversation exists, create a new one
            chat_message = Chat.objects.create(
                sender=sender, receiver=receiver, message=message)
        else:
            # If a conversation exists, append the new message to the existing conversation
            chat_message.message += f"\n{message}"
            chat_message.save()

        for file in files:
            file_obj = File.objects.create(file=file)
            chat_message.files.add(file_obj)

        serializer = ChatSerializer(chat_message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
