from rest_framework import serializers
from .models import Chat, File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'file', 'timestamp')


class ChatSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, read_only=True)  # Add File serializer

    class Meta:
        model = Chat
        fields = ('id', 'sender', 'receiver', 'message', 'files', 'timestamp')
