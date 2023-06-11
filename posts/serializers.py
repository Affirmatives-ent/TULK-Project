from .models import (Post, Comment, Share, Like)
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    comments_count = serializers.SerializerMethodField(read_only=True)
    shares_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"

    def get_likes(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_shares_count(self, obj):
        return obj.shares.count()


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.first_name", read_only=True)

    class Meta:
        model = Like
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.first_name", read_only=True)

    class Meta:
        model = Comment
        fields = ("author", "body",)


class ShareSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.first_name", read_only=True)

    class Meta:
        model = Share
        fields = "__all__"
