from django.urls import path
import uuid
from . import views

app_name = "user_groups"

urlpatterns = [
    path('groups/create/', views.CreateConversationGroup.as_view(),
         name='create_conversation_group'),
    path('groups/', views.ListConversationGroups.as_view(), name='group-list'),
    path('groups/<uuid:group_id>/invite/',
         views.InviteUserToGroup.as_view(), name='invite_user_to_group'),
    path('groups/<uuid:group_id>/invitation/',
         views.AcceptOrRejectInvitation.as_view(), name='accept_or_reject_invitation'),
    #     path('groups/<uuid:group_id>/chats/',
    #          views.GroupChatList.as_view(), name='group_chat_list'),
    path('groups/<uuid:pk>/',
         views.ConversationGroupDetail.as_view(), name='group-detail'),
    path('groups/<uuid:pk>/', views.ConversationGroupDetailUpdate.as_view(),
         name='group-detail-update'),
]
