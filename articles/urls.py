from django.urls import path
from .views import AdminArticleListView, AdminArticleDetailView, UserArticleListView, UserArticleDetailView

app_name = "articles"  # Add the 'app_name' here

urlpatterns = [
    # Admin URLs
    path('editor/articles/', AdminArticleListView.as_view(),
         name='editor-article-list'),
    path('editor/articles/<uuid:pk>/', AdminArticleDetailView.as_view(),
         name='editor-article-detail'),

    # User URLs
    path('articles/', UserArticleListView.as_view(), name='user-article-list'),
    path('articles/<uuid:pk>/', UserArticleDetailView.as_view(),
         name='user-article-detail'),
]
