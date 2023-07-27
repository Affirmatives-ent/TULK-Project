from rest_framework import serializers
from .models import Article, MediaFile


class MediaFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = "__all__"


class ArticleSerializer(serializers.ModelSerializer):
    files = MediaFileSerializer(many=True, read_only=True)
    slug = serializers.SlugField(read_only=True)  # Add the slug field here

    class Meta:
        model = Article
        fields = ('id', 'slug', 'title', 'content', 'featured_image', 'files',
                  'category', 'author', 'status', 'published_date')
