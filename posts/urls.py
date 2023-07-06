
from django.urls import path
from .views import (
    PostListCreateView,
    PostRetrieveUpdateDestroyView,
    LikeView,
    CommentListCreateView,
    ShareCreateView,
)

urlpatterns = [
    path('posts', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyView.as_view(),
         name='post-retrieve-update-destroy'),
    path('posts/<int:post_id>/like/', LikeView.as_view(), name='post-like'),
    path('posts/<int:post_id>/comment/',
         CommentListCreateView.as_view(), name='post-comment-create'),
    path('posts/<int:post_id>/share/',
         ShareCreateView.as_view(), name='post-share-create'),
]
