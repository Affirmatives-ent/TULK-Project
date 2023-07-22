from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
)
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import permissions

from .models import Article
from .serializers import ArticleSerializer


class AdminArticleListView(ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (permissions.IsAdminUser,)

    def delete(self, request, *args, **kwargs):
        article_pk = kwargs['pk']
        try:
            article = Article.objects.get(pk=article_pk)
        except Article.DoesNotExist:
            raise NotFound(f"Article with ID {article_pk} does not exist.")

        article.delete()
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        article_pk = kwargs['pk']
        try:
            article = Article.objects.get(pk=article_pk)
        except Article.DoesNotExist:
            raise NotFound(f"Article with ID {article_pk} does not exist.")

        serializer = self.get_serializer(
            article, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class AdminArticleDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (permissions.IsAdminUser,)

    def get_object(self):
        article_pk = self.kwargs['pk']
        try:
            return self.queryset.get(pk=article_pk)
        except Article.DoesNotExist:
            raise NotFound(f"Article with ID {article_pk} does not exist.")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UserArticleListView(ListAPIView):
    queryset = Article.objects.filter(status='published')
    serializer_class = ArticleSerializer
    permission_classes = (permissions.AllowAny,)


class UserArticleDetailView(RetrieveAPIView):
    queryset = Article.objects.filter(status='published')
    serializer_class = ArticleSerializer
    permission_classes = (permissions.AllowAny,)
