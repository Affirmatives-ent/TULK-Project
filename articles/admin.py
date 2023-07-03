from django.contrib import admin
from .models import Article, MediaFile


class MediaFileInline(admin.TabularInline):
    model = MediaFile
    extra = 1


class ArticleAdmin(admin.ModelAdmin):
    inlines = [MediaFileInline]


admin.site.register(Article, ArticleAdmin)
