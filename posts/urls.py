
# from django.urls import path
# import uuid
# from .views import (
#     PostListCreateView,
#     PostRetrieveUpdateDestroyAPIView,
#     CommentListCreateAPIView,
#     LikeListCreateAPIView,
#     ShareListCreateAPIView,
#     UserPostsAPIView
# )

# app_name = 'posts'

# urlpatterns = [
#     path('posts/', PostListCreateView.as_view(), name='post-list-create'),
#     path('posts/<uuid:pk>/', PostRetrieveUpdateDestroyAPIView.as_view(),
#          name='post-retrieve-update-destroy'),
#     path('users/<uuid:user_id>/posts/',
#          UserPostsAPIView.as_view(), name='user_posts'),
#     path('posts/<uuid:post_id>/comments/',
#          CommentListCreateAPIView.as_view(), name='post-comment-list-create'),
#     path('posts/<uuid:post_id>/like/',
#          LikeListCreateAPIView.as_view(), name='post-like'),
#     path('posts/<uuid:post_id>/share/',
#          ShareListCreateAPIView.as_view(), name='post-share'),
# ]


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
