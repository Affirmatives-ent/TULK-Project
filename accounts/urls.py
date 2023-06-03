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
    UserProfileDetailAPIView
)

app_name = 'accounts'

urlpatterns = [
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
]
