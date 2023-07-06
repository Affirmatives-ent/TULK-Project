from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(
        User,
        related_name="posts",
        null=True,
        on_delete=models.SET_NULL,
    )
    body = models.TextField()
    post_media = models.FileField(blank=True, null=True)
    likes = models.PositiveIntegerField(default=0)
    comments = models.PositiveIntegerField(default=0)
    shares = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.body[:20]} by {self.author.first_name}"


class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name="post_comments", on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        related_name="user_comments",
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
        Post, related_name="post_shares", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        related_name="user_shared_posts",
        null=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')

    def get_post_link(self):
        return reverse('post-retrieve-update-destroy', kwargs={'pk': self.post.pk})
        # Replace 'post-retrieve-update-destroy' with the actual URL name for the post detail view

    def __str__(self):
        return f"{self.user.username} shared {self.post}"


class Like(models.Model):
    post = models.ForeignKey(
        Post, related_name="post_likes", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        related_name="user_liked_posts",
        null=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"{self.user.username} liked {self.post}"
