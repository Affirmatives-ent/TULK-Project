from rest_framework import generics, status, pagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrSuperuserOrReadOnly
from django.db.models import F
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .models import Post, Like, Comment, Share
from .serializers import (
    PostSerializer,
    LikeSerializer,
    CommentSerializer,
    ShareSerializer
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


class LikeView(generics.CreateAPIView, generics.DestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def post(self, request, *args, **kwargs):
        post_id = self.kwargs.get('post_id')
        user = request.user

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user has already liked the post
        if Like.objects.filter(user=user, post=post).exists():
            return Response({'detail': 'You have already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new like instance
        like = Like(user=user, post=post)
        like.save()

        # Update the number of likes in the post
        post.num_likes += 1
        post.save()

        return Response({'detail': 'Post liked successfully.'}, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        post_id = self.kwargs.get('post_id')
        user = request.user

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user has liked the post
        like = Like.objects.filter(user=user, post=post).first()
        if not like:
            return Response({'detail': 'You have not liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the like instance
        like.delete()

        # Update the number of likes in the post
        post.num_likes -= 1
        post.save()

        return Response({'detail': 'Post unliked successfully.'}, status=status.HTTP_200_OK)


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)

    def post(self, request, *args, **kwargs):
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
        post.comments = F('comments') + 1
        post.save(update_fields=['comments'])

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ShareCreateView(generics.CreateAPIView):
    queryset = Share.objects.all()
    serializer_class = ShareSerializer

    def post(self, request, *args, **kwargs):
        post_id = self.kwargs.get('post_id')
        user = request.user

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, post=post)

        # Increment the number of shares in the post
        post.num_shares += 1
        post.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
