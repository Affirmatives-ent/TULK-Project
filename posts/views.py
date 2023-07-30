# from rest_framework import generics, status
# from rest_framework.response import Response
# from .models import Post, Comment, Like, Share, File
# from .serializers import PostSerializer, CommentSerializer, LikeSerializer, ShareSerializer, FileSerializer
# from django.contrib.auth import get_user_model
# from rest_framework.views import APIView
# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework.generics import ListCreateAPIView

# User = get_user_model()


# class PostListCreateView(ListCreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     parser_classes = [MultiPartParser, FormParser]

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             post = serializer.save()

#             # Process and save multiple files
#             files_data = request.FILES.getlist('files')
#             for file_data in files_data:
#                 file_instance = File(file=file_data)
#                 file_instance.save()
#                 post.files.add(file_instance)

#             headers = self.get_success_headers(serializer.data)
#             return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


# class UserPostsAPIView(APIView):
#     def get(self, request, user_id, format=None):
#         try:
#             posts = Post.objects.filter(
#                 author__id=user_id).order_by('-created_at')
#             serializer = PostSerializer(posts, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except User.DoesNotExist:
#             return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)


# class CommentListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer


# class LikeListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Like.objects.all()
#     serializer_class = LikeSerializer

#     def post(self, request, *args, **kwargs):
#         post_id = kwargs.get('post_id')
#         user = request.user

#         try:
#             post = Post.objects.get(id=post_id)
#         except Post.DoesNotExist:
#             return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

#         # Check if the user already liked the post
#         try:
#             like = Like.objects.get(user=user, post=post)
#             # If the like already exists, remove it
#             like.delete()
#             return Response({'detail': 'Like removed successfully.'}, status=status.HTTP_200_OK)
#         except Like.DoesNotExist:
#             # If the like does not exist, create it
#             like = Like.objects.create(user=user, post=post)
#             return Response({'detail': 'Like added successfully.'}, status=status.HTTP_201_CREATED)


# class ShareListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Share.objects.all()
#     serializer_class = ShareSerializer


from rest_framework import generics, status
from rest_framework.response import Response
from .models import Post, Comment, Like, Share, File
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, ShareSerializer, FileSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import ListCreateAPIView

User = get_user_model()


class PostListCreateView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save()

            # Process and save multiple files
            files_data = request.FILES.getlist('files')
            for file_data in files_data:
                file_instance = File(file=file_data)
                file_instance.save()
                post.files.add(file_instance)

            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


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
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


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
    serializer_class = LikeSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Like.objects.filter(post_id=post_id)


class ShareListCreateAPIView(generics.ListCreateAPIView):
    queryset = Share.objects.all()
    serializer_class = ShareSerializer
