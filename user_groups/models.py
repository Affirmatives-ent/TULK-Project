from django.db import models
from django.conf import settings
from accounts.models import Friendship


class ConversationGroup(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    slogan = models.CharField(max_length=255)
    about = models.TextField()
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='groupcreator')
    admin_phone = models.CharField(max_length=20)
    admin_email = models.EmailField()
    admin_website = models.URLField()
    background_image = models.ImageField(upload_to='group/backgrounds/')
    avatar = models.ImageField(upload_to='group/avatars/')
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='usergroups')

    def __str__(self):
        return self.name


class GroupInvitation(models.Model):
    group = models.ForeignKey(
        ConversationGroup, on_delete=models.CASCADE, related_name='invitations')
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_invitations')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='group_invitations')
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.invited_by.username} invited {self.user.username} to {self.group.name}'


class ConversationTopic(models.Model):
    group = models.ForeignKey(
        ConversationGroup, on_delete=models.CASCADE, related_name='topics')
    starter = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='started_topics')
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ConversationMessage(models.Model):
    topic = models.ForeignKey(
        ConversationTopic, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message by {self.author.username} in {self.topic.title}'
