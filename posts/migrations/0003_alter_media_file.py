# Generated by Django 4.2.1 on 2023-07-16 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_alter_comment_options_remove_comment_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='file',
            field=models.FileField(upload_to='post_media/'),
        ),
    ]