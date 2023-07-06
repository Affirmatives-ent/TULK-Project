from .models import Like
from .models import (Post, Comment, Share, Like)
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ShareSerializer(serializers.ModelSerializer):

    class Meta:
        model = Share
        fields = "__all__"
