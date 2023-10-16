from django.urls import path
from .views import ChatCreateView, UserChatListView, ChatConversationView

urlpatterns = [
    path('send-message/', ChatCreateView.as_view(), name='send-message'),
    # path('user-chats/', UserChatList.as_view(), name='user-chats'),
    path('chat-list/', UserChatListView.as_view(),
         name='chat-list'),
    path('chat/<int:receiver_id>/',
         ChatConversationView.as_view(), name='chat-conversation'),
]
