from autoslug import AutoSlugField
from django.db import models
from django.utils import timezone
from django.conf import settings
import uuid
from cloudinary_storage.storage import MediaCloudinaryStorage
# from django.utils.text import slugify
# from autoslug import AutoSlugField


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
        ('education', 'EDUCATION'),
        ('gossip', 'GOSSIP'),
        ('more', 'More')
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = AutoSlugField(unique=True, populate_from='title')
    content = models.TextField(blank=True)
    featured_image = models.ImageField(
        upload_to='images/', null=True, blank=True)
    files = models.ManyToManyField('MediaFile', blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft')
    published_date = models.DateTimeField(auto_now_add=True)

    def publish(self):
        self.status = 'published'
        self.published_date = timezone.now()
        self.save()

    class Meta:
        ordering = ["-published_date"]

    def __str__(self):
        return self.title[:30]


class MediaFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='article_files/',
                            storage=MediaCloudinaryStorage())
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return "Uploaded"
