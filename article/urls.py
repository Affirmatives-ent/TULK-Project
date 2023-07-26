from django.urls import path
from .views import PublishArticleView, AdminArticleListView, AdminArticleDetailView, UserArticleListView, UserArticleDetailView

app_name = "article"

urlpatterns = [

    path('publish-article/', PublishArticleView.as_view(), name='publish-article'),
    path('published-articles/', AdminArticleListView.as_view(),
         name='published-articles'),

    path('editor/articles/<uuid:pk>/', AdminArticleDetailView.as_view(),
         name='editor-article-detail'),

    path('articles/', UserArticleListView.as_view(), name='user-article-list'),
    path('articles/<uuid:pk>/', UserArticleDetailView.as_view(),
         name='user-article-detail'),
]
