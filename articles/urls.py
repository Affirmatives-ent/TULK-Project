# urls.py
from django.urls import path
from .views import (
    AdminArticleListView,
    AdminArticleDetailView,
    UserArticleListView,
    UserArticleDetailView,
)

app_name = "articles"

urlpatterns = [
    path('admin/articles/', AdminArticleListView.as_view(),
         name='admin_article_list'),
    path('admin/articles/<int:pk>/', AdminArticleDetailView.as_view(),
         name='admin_article_detail'),
    path('articles/', UserArticleListView.as_view(), name='user_article_list'),
    path('articles/<int:pk>/', UserArticleDetailView.as_view(),
         name='user_article_detail'),
    # other API URLs
]
