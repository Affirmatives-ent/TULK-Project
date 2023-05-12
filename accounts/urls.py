from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, UserProfileViewSet

router = routers.DefaultRouter()
router.register(r'accounts', UserViewSet)
router.register(r'profiles', UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
