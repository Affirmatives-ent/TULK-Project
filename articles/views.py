# views.py
from rest_framework import permissions, generics
from rest_framework.exceptions import NotFound
from .models import Article, MediaFile
from .serializers import ArticleSerializer, MediaFileSerializer


class AdminArticleListView(generics.ListAPIView):
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
        return self.update(request, *args, **kwargs)


class AdminArticleDetailView(generics.RetrieveUpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (permissions.IsAdminUser,)


class AdminMediaFilePublishView(generics.CreateAPIView):
    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer
    permission_classes = (permissions.IsAdminUser,)


class UserArticleListView(generics.ListAPIView):
    queryset = Article.objects.filter(status='published')
    serializer_class = ArticleSerializer
    permission_classes = (permissions.AllowAny,)


class UserArticleDetailView(generics.RetrieveAPIView):
    queryset = Article.objects.filter(status='published')
    serializer_class = ArticleSerializer
    permission_classes = (permissions.AllowAny,)
