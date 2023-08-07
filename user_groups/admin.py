from django.contrib import admin
from .models import ConversationGroup, GroupPost, GroupMedia, Comment, Like

admin.site.register(ConversationGroup)
admin.site.register(GroupPost)
admin.site.register(GroupMedia)
admin.site.register(Comment)
admin.site.register(Like)
