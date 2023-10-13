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
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    # Use the ListSerializer for the 'files' field
    files = FileSerializer(many=True, read_only=True)
    uploaded_files = serializers.ListField(
        child=serializers.FileField(allow_empty_file=True), write_only=True, required=False)

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'files', "uploaded_files"]

    def create(self, validated_data):
        uploaded_files = validated_data.pop('uploaded_files', [])

        post = Post.objects.create(**validated_data)

        if uploaded_files:

            for file in uploaded_files:
                File.objects.create(post=post, file=file)

        return post
