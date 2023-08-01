# from rest_framework import serializers
# from .models import Post, Like, Comment, Share, File


# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = '__all__'


# class LikeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Like
#         fields = '__all__'


# class ShareSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Share
#         fields = '__all__'


# class FileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = File
#         fields = '__all__'


# class PostSerializer(serializers.ModelSerializer):
#     files = FileSerializer(many=True, required=False)
#     comments_count = serializers.SerializerMethodField()
#     likes_count = serializers.SerializerMethodField()
#     shares_count = serializers.SerializerMethodField()

#     class Meta:
#         model = Post
#         fields = ['id', 'author', 'content', 'files', 'created_at',
#                   'likes_count', 'comments_count', 'shares_count']

#     def get_comments_count(self, obj):
#         return obj.comments.count()

#     def get_likes_count(self, obj):
#         return obj.likes.count()

#     def get_shares_count(self, obj):
#         return obj.shares.count()


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
                File.objects.create(post=post, **file_data)
        return post

    
