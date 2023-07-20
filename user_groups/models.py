from django.db import models
from django.conf import settings
from accounts.models import Friendship
import uuid
from cloudinary.models import CloudinaryField


class ConversationGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    slogan = models.CharField(max_length=255)
    about = models.TextField()
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='groupcreator', to_field='id')
    admin_phone = models.CharField(max_length=20)
    admin_email = models.EmailField()
    admin_website = models.URLField()
    background_image = CloudinaryField('group/backgrounds/')
    avatar = CloudinaryField('group/avatars/')
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='usergroups')

    def __str__(self):
        return self.name


class GroupInvitation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(
        ConversationGroup, on_delete=models.CASCADE, related_name='invitations', to_field='id')
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_invitations', to_field='id')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='group_invitations', to_field='id')
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.invited_by.username} invited {self.user.username} to {self.group.name}'


class GroupChat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(
        'ConversationGroup', on_delete=models.CASCADE, related_name='group_chat', to_field='id')
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field='id')
    message = models.TextField()
    media = CloudinaryField('group/media/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.group.name} - {self.sender.username}: {self.message}'
