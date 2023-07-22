from django.db import models
from django.utils import timezone
from django.conf import settings
import uuid


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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    featured_image = models.ImageField(
        upload_to='images/', null=True, blank=True)
    files = models.FileField(upload_to='article_media/', blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field='id')
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft')
    published_date = models.DateTimeField(null=True, blank=True)

    def publish(self):
        self.status = 'published'
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title[:30]
