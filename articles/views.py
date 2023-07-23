from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import permissions
from rest_framework import status
from .models import Article
from .serializers import ArticleSerializer


class PublishArticleView(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def post(self, request, format=None):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            # Save the article with status 'published'
            article = serializer.save(status='published')

            # Process and save multiple media files
            files_data = request.FILES.getlist('files')
            for file_data in files_data:
                article.files.create(file=file_data)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublishedArticleListView(APIView):
    def get(self, request, format=None):
        # Get both published and draft articles
        published_articles = Article.objects.filter(status='published')
        draft_articles = Article.objects.filter(status='draft')

        # Combine the two querysets and serialize the data
        articles = published_articles | draft_articles
        serializer = ArticleSerializer(articles, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


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
