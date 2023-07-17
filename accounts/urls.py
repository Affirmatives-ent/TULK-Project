from django.urls import path
import uuid
from .views import (
    UserRegistrationAPIView,
    VerifyOTPAPIView,
    #     UserListAPIView,
    #     UserDetailAPIView,
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
    NotificationListAPIView,
    NotificationUpdateAPIView,
    NotificationCountAPIView,
    ResendOTPAPIView


)

app_name = 'accounts'

urlpatterns = [
    path('', WelcomeAPIView.as_view(), name='welcome'),
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('resend-otp/', ResendOTPAPIView.as_view(), name='resend-otp'),
    path('verify-otp/<uuid:pk>/', VerifyOTPAPIView.as_view(), name='verify-otp'),
    path('logout/', UserLogoutAPIView.as_view(), name='logout'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='change-password'),
    path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot-password'),
    path('verify-password-otp/', VerifyPasswordOTPAPIView.as_view(),
         name='verify-password-otp'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),
    path('userprofiles/', UserProfileListAPIView.as_view(),
         name='userprofile-list'),
    path('userprofiles/<uuid:pk>/', UserProfileDetailAPIView.as_view(),
         name='userprofile-detail'),
    path('friend-requests/', FriendRequestListCreateAPIView.as_view(),
         name='friend-request-list-create'),
    path('friend-requests/<uuid:pk>/',
         FriendRequestRetrieveUpdateDestroyAPIView.as_view(), name='friend-request-detail'),
    path('friendships/', FriendshipListAPIView.as_view(), name='friendship-list'),
    path('friendships/create/', FriendshipCreateAPIView.as_view(),
         name='friendship-create'),
    path('notifications/', NotificationListAPIView.as_view(),
         name='notification-list'),
    path('notifications/<uuid:pk>/', NotificationUpdateAPIView.as_view(),
         name='notification-update'),
    path('notifications/count/', NotificationCountAPIView.as_view(),
         name='notification-count'),


]
