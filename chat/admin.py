from django.contrib import admin
from .models import Message, File

# Register your models here.


class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp')


class FileAdmin(admin.ModelAdmin):
    list_display = ('file', 'message')


admin.site.register(Message, MessageAdmin)
admin.site.register(File, FileAdmin)
