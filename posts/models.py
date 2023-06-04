from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(
        User,
        related_name="posts",
        null=True,
        on_delete=models.SET_NULL,
    )
    body = models.TextField()
    post_image = models.ImageField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.author}'s Post"


class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name="comments", on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        related_name="comments",
        null=True,
        on_delete=models.SET_NULL,
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.body[:20]} by {self.author.first_name}"


class Share(models.Model):
    post = models.ForeignKey(
        Post, related_name="shares", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        related_name="shared_posts",
        null=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"{self.user.username} shared {self.post}"


class Like(models.Model):
    post = models.ForeignKey(
        Post, related_name="likes", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        related_name="liked_posts",
        null=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"{self.user.username} liked {self.post}"
