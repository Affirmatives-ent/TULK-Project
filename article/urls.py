from django.urls import path
from .views import (
    PublishArticleView,
    AdminArticleListView,
    AdminArticleDetailView,
    UserArticleListView,
    UserArticleDetailView,
)

app_name = 'article'

urlpatterns = [
    # URLs for admin users
    # URL for publishing articles (admin only)
    path('editor/publish-article/',
         PublishArticleView.as_view(), name='publish-article'),
    path('editor/articles/', AdminArticleListView.as_view(),
         name='admin-article-list'),
    #     path('editor/articles/<uuid:pk>/',
    #          AdminArticleDetailView.as_view(), name='admin-article-detail'),
    path('articles/<slug:slug>/',
         AdminArticleDetailView.as_view(), name='article_detail'),
    # URLs for all users
    path('articles/', UserArticleListView.as_view(), name='user-article-list'),
    path('articles/<uuid:pk>/', UserArticleDetailView.as_view(),
         name='user-article-detail'),
]
