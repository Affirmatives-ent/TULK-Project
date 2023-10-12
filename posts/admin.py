from django.contrib import admin

from .models import Post, Comment, Like, Share, File


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author',)
    list_filter = ('author',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post',)
    list_filter = ('user',)


class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'post')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(File, FileAdmin)


admin.site.register(Like)
admin.site.register(Share)
