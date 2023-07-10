from django.contrib import admin
from articles.models import Article, MediaFile


admin.site.register(Article)
admin.site.register(MediaFile)
