# Generated by Django 4.2.1 on 2023-08-24 11:14

import cloudinary_storage.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_notification_content_type_notification_object_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, storage=cloudinary_storage.storage.MediaCloudinaryStorage(), upload_to='user_avatar/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='background_image',
            field=models.ImageField(blank=True, null=True, storage=cloudinary_storage.storage.MediaCloudinaryStorage(), upload_to='cover_image/'),
        ),
    ]