from django.db import models
from django.contrib.auth import get_user_model
import uuid
from cloudinary_storage.storage import MediaCloudinaryStorage
from django.conf import settings
User = get_user_model()


class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages', to_field='id')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_messages', to_field='id')
    message = models.TextField()
    files = models.ManyToManyField('File', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"{self.sender} -- {self.receiver}: {self.message[:20]}"


class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='messages_files/',
                            storage=MediaCloudinaryStorage())

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return "Media file added"
