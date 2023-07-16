
from django.urls import path
import uuid
from .views import (
    PostListCreateView,
    PostRetrieveUpdateDestroyView,
    LikeView,
    CommentListCreateView,
    ShareView,
)

app_name = 'posts'

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<uuid:pk>/', PostRetrieveUpdateDestroyView.as_view(),
         name='post-retrieve-update-destroy'),
    path('posts/<uuid:post_id>/like/', LikeView.as_view(), name='post-like'),
    path('posts/<uuid:post_id>/comments/', CommentListCreateView.as_view(),
         name='post-comment-list-create'),
    path('posts/<uuid:post_id>/share/', ShareView.as_view(), name='post-share'),
]
