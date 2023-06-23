from django.contrib import admin

from .models import User, UserProfile, Friendship, FriendRequest, Notification, ConversationGroup, GroupInvitation

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Friendship)
admin.site.register(FriendRequest)
admin.site.register(Notification)
admin.site.register(ConversationGroup)
admin.site.register(GroupInvitation)
