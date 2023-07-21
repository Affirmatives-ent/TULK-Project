
from django.urls import path
import uuid
from .views import (
    PostListCreateAPIView,
    PostRetrieveUpdateDestroyAPIView,
    CommentListCreateAPIView,
    LikeListCreateAPIView,
    ShareListCreateAPIView,
    UserPostsAPIView
)

app_name = 'posts'

urlpatterns = [
    path('posts/', PostListCreateAPIView.as_view(), name='post-list-create'),
    path('posts/<uuid:pk>/', PostRetrieveUpdateDestroyAPIView.as_view(),
         name='post-retrieve-update-destroy'),
    path('users/<uuid:user_id>/posts/',
         UserPostsAPIView.as_view(), name='user_posts'),
    path('posts/<uuid:post_id>/comments/',
         CommentListCreateAPIView.as_view(), name='post-comment-list-create'),
    path('posts/<uuid:post_id>/like/',
         LikeListCreateAPIView.as_view(), name='post-like'),
    path('posts/<uuid:post_id>/share/',
         ShareListCreateAPIView.as_view(), name='post-share'),
]
