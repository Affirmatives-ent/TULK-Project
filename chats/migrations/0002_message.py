# Generated by Django 3.2.7 on 2023-10-20 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='status',
            field=models.CharField(
                choices=[('read', 'Read'), ('unread', 'Unread')], default='unread', max_length=10),
        ),
    ]
