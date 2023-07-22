from django.urls import path
from .views import AdminArticleListView, AdminArticleDetailView, UserArticleListView, UserArticleDetailView

app_name = "articles"  # Add the 'app_name' here

urlpatterns = [
    # Admin URLs
    path('admin/articles/', AdminArticleListView.as_view(),
         name='admin-article-list'),
    path('admin/articles/<uuid:pk>/', AdminArticleDetailView.as_view(),
         name='admin-article-detail'),

    # User URLs
    path('articles/', UserArticleListView.as_view(), name='user-article-list'),
    path('articles/<uuid:pk>/', UserArticleDetailView.as_view(),
         name='user-article-detail'),
]
