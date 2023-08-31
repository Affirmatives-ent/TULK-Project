from django.contrib import admin

from .models import Post, Comment, Like, Share


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content')
    list_filter = ('author')


admin.site.register(Post, PostAdmin)


admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Share)
