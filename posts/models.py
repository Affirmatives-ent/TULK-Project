from django.contrib.auth import get_user_model
from django.db import models
import uuid

User = get_user_model()


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts', to_field='id')
    # Add any other fields you need


class Media(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='media', to_field='id')
    file = models.FileField(upload_to='post_media/')


class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='id')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='likes', to_field='id')


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='id')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments', to_field='id')
    content = models.TextField()


class Share(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='id')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='shares', to_field='id')
