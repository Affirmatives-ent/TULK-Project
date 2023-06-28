from rest_framework import serializers
from .models import Article, MediaFile


class MediaFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = "__all__"


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"

    def create(self, validated_data):
        media_files_data = validated_data.pop('media_files', [])
        article = Article.objects.create(**validated_data)

        for media_file_data in media_files_data:
            MediaFile.objects.create(article=article, **media_file_data)

        return article
