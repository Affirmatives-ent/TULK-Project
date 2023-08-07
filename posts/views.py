
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, ShareSerializer, FileSerializer
from .models import Post, Comment, Like, Share, File
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
User = get_user_model()


class PostListCreateView(APIView):
    # Add the IsAuthenticated permission class
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    # Add the PageNumberPagination class and specify the page size
    pagination_class = PageNumberPagination
    page_size = 10  # Set the desired number of items per page

    def get(self, request, format=None):
        # Fetch all posts from the database
        posts = Post.objects.all()
        # Serialize the posts and convert them to JSON data
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(result_page, many=True)
        # Get the JSON data
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save()

            # Process and save multiple files
            files_data = request.FILES.getlist('files')
            for file_data in files_data:
                file_instance = File(file=file_data)
                file_instance.save()
                post.files.add(file_instance)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]


class UserPostsAPIView(APIView):
    def get(self, request, user_id, format=None):
        try:
            posts = Post.objects.filter(
                author__id=user_id).order_by('-created_at')
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)


class CommentListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        # Get the post ID from the URL parameter
        post_id = self.kwargs.get('post_id')
        # Get the post object based on the post ID
        post = get_object_or_404(Post, id=post_id)
        # Filter the comments queryset based on the post object
        queryset = Comment.objects.filter(post=post)
        return queryset


class LikeToggleAPIView(APIView):
    def post(self, request, post_id, format=None):
        user = request.user

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user already liked the post
        try:
            like = Like.objects.get(user=user, post=post)
            # If the like already exists, remove it
            like.delete()
            return Response({'detail': 'Like removed successfully.'}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            # If the like does not exist, create it
            like = Like.objects.create(user=user, post=post)
            return Response({'detail': 'Like added successfully.'}, status=status.HTTP_201_CREATED)


class LikeListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Like.objects.filter(post_id=post_id)


class ShareListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Share.objects.all()
    serializer_class = ShareSerializer
