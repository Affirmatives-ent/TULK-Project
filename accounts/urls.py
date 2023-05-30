from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserRegistrationAPIView,
    VerifyOTPAPIView,
    UserAPIView,
    UserLogoutAPIView,
    UserProfileAPIView,
    ChangePasswordAPIView,
    ForgotPasswordAPIView,
    VerifyPasswordOTPAPIView,
    ResetPasswordAPIView
)

app_name = 'accounts'

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('verify-otp/<int:pk>/', VerifyOTPAPIView.as_view(), name='verify-otp'),
    path('users/', UserAPIView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserAPIView.as_view(), name='user-detail'),
    path('logout/', UserLogoutAPIView.as_view(), name='logout'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='change-password'),
    path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot-password'),
    path('verify-password-otp/', VerifyPasswordOTPAPIView.as_view(),
         name='verify-password-otp'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),
    path('user-profile/', UserProfileAPIView.as_view(), name='user-profile'),
    path('api/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
