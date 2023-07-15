from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    post_media = models.FileField(
        upload_to='post_media/', null=True, blank=True)
    likes = models.ManyToManyField(
        User, related_name='liked_posts', null=True, blank=True)
    comments = models.PositiveIntegerField(default=0)
    shares = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Post {self.id} by {self.author.username}"


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        related_name="post_comments",  # Specify a related_name to avoid clash
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        related_name="user_comments",
        null=True,
        on_delete=models.SET_NULL,
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.content[:20]} by {self.author.username}"
