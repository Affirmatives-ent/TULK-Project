# from django.contrib.auth import get_user_model
# from django.db import models
# import uuid

# User = get_user_model()


# class Post(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     content = models.TextField(blank=True)
#     files = models.ManyToManyField('File', blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     author = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name='posts', to_field='id')

#     class Meta:
#         ordering = ["-created_at"]

#     def __str__(self):
#         return self.content[:20]


# class File(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     file = models.FileField(upload_to='post_files/')
#     uploaded_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ["-uploaded_at"]

#     def __str__(self):
#         return "Updloaded"


# class Like(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='id')
#     post = models.ForeignKey(
#         Post, on_delete=models.CASCADE, related_name='likes', to_field='id')
#     liked_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ["-liked_at"]

#     def __str__(self):
#         return f"{self.user} liked {self.post.author}\'s post"


# class Comment(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='id')
#     post = models.ForeignKey(
#         Post, on_delete=models.CASCADE, related_name='comments', to_field='id')
#     content = models.TextField()

#     commented_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ["-commented_at"]

#     def __str__(self):
#         return self.content[:20]


# class Share(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='id')
#     post = models.ForeignKey(
#         Post, on_delete=models.CASCADE, related_name='shares', to_field='id')


from django.contrib.auth import get_user_model
from django.db import models
import uuid

User = get_user_model()


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(blank=True)
    files = models.ManyToManyField('File', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts', to_field='id')

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.content[:20]


class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='post_files/')
    # post = models.ForeignKey(
    #     Post, on_delete=models.CASCADE, related_name='files')

    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return "Uploaded"


class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='id')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='likes', to_field='id')
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-liked_at"]

    def __str__(self):
        return f"{self.user} liked {self.post.author}'s post"


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='id')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments', to_field='id')
    content = models.TextField()

    commented_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-commented_at"]

    def __str__(self):
        return self.content[:20]


class Share(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='id')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='shares', to_field='id')
    shared_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-shared_at"]

    def __str__(self):
        return f"{self.user} shared {self.post.author}'s post"
