from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
import uuid
from cloudinary.models import CloudinaryField


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
    featured_image = CloudinaryField('images/', null=True, blank=True)
    media = CloudinaryField('media/')
    categories = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
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


class MediaFile(models.Model):

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
    caption = models.CharField(max_length=100, null=True, blank=True)
    file = CloudinaryField('media/')
    categories = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field='id')
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft')
    published_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.caption
