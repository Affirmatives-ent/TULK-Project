from rest_framework import serializers
from .models import Message, File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, read_only=True)
    uploaded_files = serializers.ListField(
        child=serializers.FileField(allow_empty_file=True), write_only=True, required=False)

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message_content',
                  'files', 'uploaded_files', 'timestamp']

    def create(self, validated_data):
        uploaded_files = validated_data.pop('uploaded_files', [])
        message = Message.objects.create(**validated_data)
        if uploaded_files:
            for file in uploaded_files:
                File.objects.create(message=message, file=file)
        return message
