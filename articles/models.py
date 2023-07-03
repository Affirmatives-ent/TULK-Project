from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings


class Article(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    CATEGORY_CHOICES = (
        ('politics', 'Politics'),
        ('sport', 'Sport'),
        ('entertainment', 'Entertainment'),
        ('metro', 'Metro'),
        ('more', 'More'),
    )
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    featured_image = models.ImageField(
        upload_to='images/', null=True, blank=True)
    categories = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft')
    published_date = models.DateTimeField(null=True, blank=True)

    def publish(self):
        self.status = 'published'
        self.published_date = timezone.now()
        self.save()


class MediaFile(models.Model):
    caption = models.CharField(max_length=100)
    file = models.FileField(upload_to='media/')
    article = models.ForeignKey(
        Article, on_delete=models.SET_NULL, null=True, blank=True, related_name='media_files')
    published_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    published_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.file.name
