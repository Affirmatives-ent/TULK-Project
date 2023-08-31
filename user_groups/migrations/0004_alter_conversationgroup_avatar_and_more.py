# Generated by Django 4.2.1 on 2023-08-24 11:14

import cloudinary_storage.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_groups', '0003_rename_media_grouppost_files'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversationgroup',
            name='avatar',
            field=models.ImageField(blank=True, null=True, storage=cloudinary_storage.storage.MediaCloudinaryStorage(), upload_to='group/avatars/'),
        ),
        migrations.AlterField(
            model_name='conversationgroup',
            name='background_image',
            field=models.ImageField(blank=True, null=True, storage=cloudinary_storage.storage.MediaCloudinaryStorage(), upload_to='group/backgrounds/'),
        ),
        migrations.AlterField(
            model_name='groupmedia',
            name='file',
            field=models.FileField(storage=cloudinary_storage.storage.MediaCloudinaryStorage(), upload_to='post_files/'),
        ),
    ]