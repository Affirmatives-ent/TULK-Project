from django.urls import path
from chat.views import (
    MessageListView,
    UnreadMessageCountView,
    FriendsListView,
    SendMessageView,
)

urlpatterns = [
    path('messages/<uuid:user_id>/',
         MessageListView.as_view(), name='message_list'),
    path('unread-messages/', UnreadMessageCountView.as_view(),
         name='unread_messages'),
    path('friends/<uuid:user_id>/', FriendsListView.as_view(), name='friends_list'),
    path('send-message/<uuid:user_id>/',
         SendMessageView.as_view(), name='send_message'),
]
