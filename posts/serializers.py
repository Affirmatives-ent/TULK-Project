from rest_framework import serializers
from .models import Post, Comment, Like, Share, File


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Share
        fields = '__all__'


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'file', 'post')


class PostSerializer(serializers.ModelSerializer):
    # Use the ListSerializer for the 'files' field
    files = FileSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'files', 'created_at']
