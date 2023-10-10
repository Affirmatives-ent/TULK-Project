from django.db import models
from django.contrib.auth import get_user_model
import uuid
from cloudinary_storage.storage import MediaCloudinaryStorage
from django.conf import settings
User = get_user_model()


class Chat(models.Model):
    messages = models.ManyToManyField(
        'Message', related_name='chat', blank=True)

    @property
    def last_message(self):
        return self.messages.last()

    def get_or_create_message(self, sender, receiver, message_content, files=None):
        # Create a new message or get an existing one
        message, created = Message.objects.get_or_create(
            sender=sender, receiver=receiver, message_content=message_content
        )

        if files:
            message.files.add(*files)

        # Add the message to the chat
        self.messages.add(message)

        return message

    def get_messages(self):
        return self.messages.all().order_by('timestamp')


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_messages')
    message_content = models.TextField()
    files = models.ManyToManyField(
        'File', related_name='messages', storage=MediaCloudinaryStorage())
    timestamp = models.DateTimeField(auto_now_add=True)


class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='messages_files/',
                            storage=MediaCloudinaryStorage())

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return "Media file added"
