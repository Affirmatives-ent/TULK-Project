from rest_framework import serializers
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    num_likes = serializers.SerializerMethodField(read_only=True)
    num_comments = serializers.SerializerMethodField(read_only=True)
    num_shares = serializers.SerializerMethodField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'post_media', 'likes',
                  'num_likes', 'num_comments', 'num_shares', 'comments']
        read_only_fields = ['author', 'num_likes',
                            'num_comments', 'num_shares', 'comments']

    def get_num_likes(self, instance):
        return instance.likes.count()

    def get_num_comments(self, instance):
        comments = getattr(instance, 'comments', None)
        if comments is not None:
            if isinstance(comments, int):
                return comments
            return comments.count()
        return 0

    def get_num_shares(self, instance):
        return instance.shares.count()


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content']
        read_only_fields = ['id', 'author']


class LikeSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()
