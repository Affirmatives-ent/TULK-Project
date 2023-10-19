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
from .models import Article, MediaFile
from .serializers import ArticleSerializer
from .pagination import CustomPageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser


# class PublishArticleView(APIView):
#     permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
#     parser_classes = [MultiPartParser, FormParser]

#     def post(self, request, format=None):
#         serializer = ArticleSerializer(data=request.data)
#         if serializer.is_valid():
#             article = serializer.save(status='published')

#             try:
#                 # Process and save multiple media files
#                 files_data = request.FILES.getlist('files')
#                 for file_data in files_data:
#                     file_instance = MediaFile(file=file_data)
#                     file_instance.save()
#                     article.files.add(file_instance)
#             except Exception as e:
#                 return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PublishArticleView(APIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        status = request.data.get('status', 'draft')
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            article = serializer.save(status=status)

            try:
                # Process and save multiple media files
                files_data = request.FILES.getlist('files')
                for file_data in files_data:
                    file_instance = MediaFile(file=file_data)
                    file_instance.save()
                    article.files.add(file_instance)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminArticleListView(APIView):
    permission_classes = [permissions.IsAdminUser]
    pagination_class = CustomPageNumberPagination

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
        slug = self.kwargs['slug']
        try:
            return self.queryset.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound(f"Article with slug '{slug}' does not exist.")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UserArticleListView(ListAPIView):
    queryset = Article.objects.filter(status='published')
    serializer_class = ArticleSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = CustomPageNumberPagination


class UserArticleDetailView(RetrieveAPIView):
    queryset = Article.objects.filter(status='published')
    serializer_class = ArticleSerializer
    permission_classes = (permissions.AllowAny,)
