
from django.urls import path
from .views import (
    PostListCreateView,
    PostRetrieveUpdateDestroyView,
    LikeCreateView,
    LikeDestroyView,
    CommentCreateView,
    CommentUpdateDestroyView,
    ShareCreateView,
    ShareDestroyView,
)

urlpatterns = [
    path('posts', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyView.as_view(),
         name='post-retrieve-update-destroy'),
    path('posts/<int:post_id>/like/',
         LikeCreateView.as_view(), name='post-like-create'),
    path('posts/<int:post_id>/like/<int:pk>/',
         LikeDestroyView.as_view(), name='post-like-destroy'),
    path('posts/<int:post_id>/comment/',
         CommentCreateView.as_view(), name='post-comment-create'),
    path('posts/<int:post_id>/comment/<int:pk>/',
         CommentUpdateDestroyView.as_view(), name='post-comment-update-destroy'),
    path('posts/<int:post_id>/share/',
         ShareCreateView.as_view(), name='post-share-create'),
    path('posts/<int:post_id>/share/<int:pk>/',
         ShareDestroyView.as_view(), name='post-share-destroy'),
]
