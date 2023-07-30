#

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
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'files', 'created_at']

    def create(self, validated_data):
        files_data = validated_data.pop('files', None)
        post = Post.objects.create(**validated_data)
        if files_data:
            for file_data in files_data:
                file_instance = File.objects.create(file=file_data)
                post.files.add(file_instance)
        return post
