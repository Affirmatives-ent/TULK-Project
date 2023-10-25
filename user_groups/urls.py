from django.urls import path
import uuid
from . import views
from .views import (
    GroupPostListCreateView,
    PostRetrieveUpdateDestroyAPIView,
    UserPostsAPIView,
    CommentListCreateAPIView,
    LikeToggleAPIView,
    LikeListAPIView,
    UserGroupsAPIView
)

app_name = "user_groups"

urlpatterns = [
    path('groups/create/', views.CreateConversationGroup.as_view(),
         name='create_conversation_group'),
    path('groups/', views.ListConversationGroups.as_view(), name='group-list'),
    path('groups/<uuid:group_id>/invite/',
         views.InviteUserToGroup.as_view(), name='invite_user_to_group'),
    path('groups/<uuid:invitation_id>/',
         views.AcceptOrRejectInvitation.as_view(), name='accept_or_reject_invitation'),
    path('group/<uuid:group_id>/posts/', GroupPostListCreateView.as_view(),
         name='group-post-list-create'),
    path('group-posts/<uuid:pk>/', PostRetrieveUpdateDestroyAPIView.as_view(),
         name='post-retrieve-update-destroy'),
    path('group-posts/<uuid:group_id>/user-posts/',
         UserPostsAPIView.as_view(), name='user-posts'),
    path('group-posts/<uuid:post_id>/comments/',
         CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('group-posts/<uuid:post_id>/like-toggle/',
         LikeToggleAPIView.as_view(), name='like-toggle'),
    path('group-posts/<uuid:post_id>/likes/',
         LikeListAPIView.as_view(), name='like-list'),
    path('groups/<uuid:pk>/', views.ConversationGroupDetail.as_view(),
         name='group-detail'),
    #     path('groups/<uuid:group_id>/',
    #          views.ConversationGroupDetail.as_view(), name='group-detail'),
    path('user-groups/', UserGroupsAPIView.as_view(), name='user-groups'),
]
