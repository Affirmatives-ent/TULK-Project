# Generated by Django 4.2.1 on 2023-08-01 20:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_alter_article_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.CharField(choices=[('politics', 'Politics'), ('sport', 'Sport'), ('entertainment', 'Entertainment'), ('metro', 'Metro'), ('education', 'EDUCATION'), ('gossip', 'GOSSIP'), ('more', 'More')], max_length=20),
        ),
        migrations.AlterField(
            model_name='article',
            name='published_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]