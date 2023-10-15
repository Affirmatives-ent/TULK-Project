from django.urls import path
from .views import ChatCreateView, UserChatList, ConversationListView

urlpatterns = [
    path('send-message/', ChatCreateView.as_view(), name='send-message'),
    path('user-chats/', UserChatList.as_view(), name='user-chats'),
    path('conversations/', ConversationListView.as_view(),
         name='conversation-list'),
]
