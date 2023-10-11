from django.contrib import admin

from .models import User, Friendship, FriendRequest, Notification, ProfileMedia


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'email',)
    list_filter = ('first_name', )


class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('user1', 'user2', 'created_at',)


class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ("sender", "recipient", 'accepted',)
    list_filter = ('accepted',)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'type',)
    list_filter = ('type',)


class ProfileMediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',)


admin.site.register(User, UserAdmin)
admin.site.register(Friendship, FriendshipAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(ProfileMedia, ProfileMediaAdmin)
