from django.contrib.auth import get_user_model
from django.db import models
import uuid

User = get_user_model()


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, to_field='id')
    content = models.TextField(null=True, blank=True)
    post_media = models.FileField(
        upload_to='post_media/', null=True, blank=True)
    likes = models.ManyToManyField(
        User, related_name='liked_posts', null=True, blank=True)
    comments = models.PositiveIntegerField(default=0)
    shares = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Post {self.id} by {self.author.username}"


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(
        Post,
        related_name="post_comments",  # Specify a related_name to avoid clash
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        related_name="user_comments",
        null=True,
        on_delete=models.SET_NULL, to_field='id'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.content[:20]} by {self.author.username}"
