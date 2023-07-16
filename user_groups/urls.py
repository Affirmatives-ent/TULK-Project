from django.urls import path
import uuid
from . import views

app_name = "user_groups"

urlpatterns = [
    path('groups/create/', views.CreateConversationGroup.as_view(),
         name='create_conversation_group'),
    path('groups/<uuid:group_id>/invite/',
         views.InviteUserToGroup.as_view(), name='invite_user_to_group'),
    path('friends/search/', views.FriendSearch.as_view(), name='friend_search'),
    path('groups/<uuid:group_id>/invitation/',
         views.AcceptOrRejectInvitation.as_view(), name='accept_or_reject_invitation'),
    path('groups/<uuid:group_id>/chats/',
         views.GroupChatList.as_view(), name='group_chat_list'),
]
