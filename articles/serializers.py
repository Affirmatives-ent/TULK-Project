from rest_framework import serializers
from .models import Article, MediaFile


class MediaFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = ('file', 'uploaded_at')


class ArticleSerializer(serializers.ModelSerializer):
    files = MediaFileSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'featured_image', 'files',
                  'category', 'author', 'status', 'published_date')
