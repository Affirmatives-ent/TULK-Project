from django.db import models
from django.conf import settings
from accounts.models import Friendship
from django.contrib.auth import get_user_model
import uuid
User = get_user_model()


class ConversationGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    slogan = models.CharField(max_length=255, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    admin = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='groupcreator', to_field='id')
    admin_phone = models.CharField(max_length=20, blank=True, null=True)
    admin_email = models.EmailField(blank=True, null=True)
    admin_website = models.URLField(blank=True, null=True)
    background_image = models.ImageField(
        upload_to='group/backgrounds/', blank=True, null=True)
    avatar = models.ImageField(
        upload_to='group/avatars/', blank=True, null=True)
    members = models.ManyToManyField(
        User, related_name='usergroups', blank=True, null=True)

    def __str__(self):
        return self.name


class GroupInvitation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(
        ConversationGroup, on_delete=models.CASCADE, related_name='invitations', to_field='id')
    invited_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_invitations', to_field='id')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='group_invitations', to_field='id')
    is_accepted = models.BooleanField(default=False)
    invited_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-invited_at"]

    def __str__(self):
        return f'{self.invited_by.username} invited {self.user.username} to {self.group.name}'


class GroupPost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(
        'ConversationGroup', on_delete=models.CASCADE, related_name='group_post', to_field='id')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, to_field='id')
    content = models.TextField(blank=True)
    media = models.ManyToManyField('GroupMedia', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f'{self.group.name} - {self.author.first_name}: {self.content}'


class GroupMedia(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='post_files/')
    # post = models.ForeignKey(
    #     Post, on_delete=models.CASCADE, related_name='files')

    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return "Uploaded"


class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(
        'ConversationGroup', on_delete=models.CASCADE, related_name='group_post_like', to_field='id')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='group_post_liker', to_field='id')
    post = models.ForeignKey(
        GroupPost, on_delete=models.CASCADE, related_name='likes', to_field='id')
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-liked_at"]

    def __str__(self):
        return f"{self.user} liked {self.post.author}'s post"


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(
        'ConversationGroup', on_delete=models.CASCADE, related_name='group_post_comment', to_field='id')
    commenter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='group_post_commentor', to_field='id')
    post = models.ForeignKey(
        GroupPost, on_delete=models.CASCADE, related_name='comments', to_field='id')
    content = models.TextField()

    commented_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-commented_at"]

    def __str__(self):
        return self.content[:20]
