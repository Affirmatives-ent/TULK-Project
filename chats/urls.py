from django.urls import path
from .views import ChatCreateView, UserChatList, ChatConversationView

urlpatterns = [
    path('send-message/', ChatCreateView.as_view(), name='send-message'),
    path('user-chats/', UserChatList.as_view(), name='user-chats'),
    path('chat/<uuid:receiver_id>/',
         ChatConversationView.as_view(), name='chat-conversation'),
]
