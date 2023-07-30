
from django.urls import path
from .views import (
    PostListCreateView,
    PostRetrieveUpdateDestroyAPIView,
    UserPostsAPIView,
    CommentListCreateAPIView,
    LikeToggleAPIView,
    ShareListCreateAPIView,
)

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<uuid:pk>/', PostRetrieveUpdateDestroyAPIView.as_view(),
         name='post-retrieve-update-destroy'),
    path('users/<uuid:user_id>/posts/',
         UserPostsAPIView.as_view(), name='user-posts'),
    path('posts/<uuid:post_id>/comments/',
         CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('posts/<uuid:post_id>/like/',
         LikeToggleAPIView.as_view(), name='like-list-create'),
    path('posts/<uuid:post_id>/share/',
         ShareListCreateAPIView.as_view(), name='share-list-create'),
]
