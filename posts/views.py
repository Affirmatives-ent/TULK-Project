from rest_framework import generics, status, pagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrSuperuserOrReadOnly
from django.db.models import F
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .models import Post, Comment
from .serializers import (
    PostSerializer,
    CommentCreateSerializer,
    LikeSerializer
)


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = pagination.PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrSuperuserOrReadOnly]


class LikeView(generics.GenericAPIView):
    serializer_class = LikeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post_id = serializer.validated_data['post_id']

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)
            post.save()
            return Response({'detail': 'Post unliked.', 'num_likes': post.likes.count()}, status=status.HTTP_200_OK)
        else:
            post.likes.add(user)
            post.save()
            return Response({'detail': 'Post liked.', 'num_likes': post.likes.count()}, status=status.HTTP_200_OK)


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentCreateSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)

    def create(self, request, *args, **kwargs):
        post_id = self.kwargs.get('post_id')
        user = request.user

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post, author=user)

        # Increment the number of comments in the post
        post.comments += 1
        post.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ShareView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        post_id = request.data.get('post_id')

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        post.shares += 1
        post.save()

        return Response({'detail': 'Post shared.', 'num_shares': post.shares}, status=status.HTTP_200_OK)
