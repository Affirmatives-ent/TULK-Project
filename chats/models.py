from django.db import models
from django.contrib.auth import get_user_model
import uuid
from cloudinary_storage.storage import MediaCloudinaryStorage
from django.conf import settings
User = get_user_model()

MESSAGE_STATUS = (
    ('read', 'Read'),
    ('unread', 'Unread')
)


class Message(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_messages')
    message_content = models.TextField()
    status = models.CharField(
        max_length=10, choices=MESSAGE_STATUS, default='unread')
    timestamp = models.DateTimeField(auto_now_add=True)


class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='messages_files/',
                            storage=MediaCloudinaryStorage(), blank=True, null=True)
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="files")

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return "Media file added"


class Conversations(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participant1 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='conversation_participant1')
    participant2 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='conversation_participant2')
    last_message = models.TextField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.participant1} ==> {self.participant2}"
