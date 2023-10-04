from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.ChatListView.as_view(), name='chat-list'),
    path('chat/<uuid:receiver_id>/',
         views.ChatConversationListView.as_view(), name='chat-list'),
    path('chat/<uuid:pk>/', views.ChatDetailView.as_view(), name='chat-detail'),
]
