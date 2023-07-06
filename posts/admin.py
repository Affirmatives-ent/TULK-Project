from django.contrib import admin

from .models import Post, Comment, Share, Like

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Share)
