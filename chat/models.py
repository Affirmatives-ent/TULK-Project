from django.db import models
from django.contrib.auth import get_user_model
import uuid
from cloudinary.models import CloudinaryField


User = get_user_model()


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages', to_field='id')
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_messages', to_field='id')
    content = models.TextField(null=True, blank=True)
    file = CloudinaryField('media/')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('timestamp',)
