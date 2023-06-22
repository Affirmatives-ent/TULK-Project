from django.urls import path
from .views import (
    UserRegistrationAPIView,
    VerifyOTPAPIView,
    UserListAPIView,
    UserDetailAPIView,
    UserLogoutAPIView,
    ChangePasswordAPIView,
    ForgotPasswordAPIView,
    VerifyPasswordOTPAPIView,
    ResetPasswordAPIView,
    UserProfileListAPIView,
    UserProfileDetailAPIView,
    WelcomeAPIView,
    FriendRequestListCreateAPIView,
    FriendRequestRetrieveUpdateDestroyAPIView,
    FriendshipListAPIView,
    FriendshipCreateAPIView,
    FriendshipDestroyAPIView,
    NotificationListAPIView
)

app_name = 'accounts'

urlpatterns = [
    path('', WelcomeAPIView.as_view(), name='welcome'),
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('verify-otp/<int:pk>/', VerifyOTPAPIView.as_view(), name='verify-otp'),
    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'),
    path('logout/', UserLogoutAPIView.as_view(), name='logout'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='change-password'),
    path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot-password'),
    path('verify-password-otp/', VerifyPasswordOTPAPIView.as_view(),
         name='verify-password-otp'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),
    path('userprofiles/', UserProfileListAPIView.as_view(),
         name='userprofile-list'),
    path('userprofiles/<int:pk>/', UserProfileDetailAPIView.as_view(),
         name='userprofile-detail'),
    path('friend-requests/', FriendRequestListCreateAPIView.as_view(),
         name='friend-request-list-create'),
    path('friend-requests/<int:pk>/', FriendRequestRetrieveUpdateDestroyAPIView.as_view(),
         name='friend-request-retrieve-update-destroy'),
    path('friendships/', FriendshipListAPIView.as_view(), name='friendship-list'),
    path('friendships/create/', FriendshipCreateAPIView.as_view(),
         name='friendship-create'),
    path('friendships/<int:pk>/destroy/',
         FriendshipDestroyAPIView.as_view(), name='friendship-destroy'),
    path('notifications/', NotificationListAPIView.as_view(),
         name='notification-list'),

]
