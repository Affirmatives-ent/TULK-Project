# Generated by Django 4.2.1 on 2023-07-03 09:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_conversationgroup_groupinvitation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=30, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must be 13 digits only!', regex='^\\d{10}')]),
        ),
    ]