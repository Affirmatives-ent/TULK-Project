# Generated by Django 4.2.1 on 2023-07-22 03:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_rename_categories_article_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='file',
        ),
        migrations.RemoveField(
            model_name='mediafile',
            name='author',
        ),
        migrations.RemoveField(
            model_name='mediafile',
            name='caption',
        ),
        migrations.RemoveField(
            model_name='mediafile',
            name='category',
        ),
        migrations.RemoveField(
            model_name='mediafile',
            name='published_date',
        ),
        migrations.RemoveField(
            model_name='mediafile',
            name='status',
        ),
        migrations.AddField(
            model_name='article',
            name='files',
            field=models.ManyToManyField(blank=True, to='articles.mediafile'),
        ),
        migrations.AddField(
            model_name='mediafile',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mediafile',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='media/'),
        ),
        migrations.AlterField(
            model_name='mediafile',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
