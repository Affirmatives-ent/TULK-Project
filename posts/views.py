from rest_framework import generics, status
from rest_framework.response import Response
from .models import Post, Comment, Like, Share
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, ShareSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class UserPostsAPIView(generics.APIView):
    def get(self, request, user_id, format=None):
        try:
            posts = Post.objects.filter(
                author__id=user_id).order_by('-created_at')
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)


class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class LikeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('post_id')
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


class ShareListCreateAPIView(generics.ListCreateAPIView):
    queryset = Share.objects.all()
    serializer_class = ShareSerializer
