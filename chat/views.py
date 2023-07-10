from rest_framework.views import APIView
from rest_framework.response import Response
from chat.models import Message
from chat.serializers import MessageSerializer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Q
from accounts.models import Friendship

User = get_user_model()


class MessageListView(APIView):
    def get(self, request, user_id):
        user = request.user
        other_user = get_object_or_404(User, id=user_id)

        messages = Message.objects.filter(
            (Q(sender=user) & Q(recipient=other_user)) | (
                Q(sender=other_user) & Q(recipient=user))
        ).order_by('timestamp')

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class UnreadMessageCountView(APIView):
    def get(self, request):
        user = request.user
        unread_count = Message.objects.filter(
            recipient=user, is_read=False).count()

        return Response({'unread_count': unread_count})


class FriendsListView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        friend_ids = Friendship.objects.filter(
            Q(user1=user) | Q(user2=user)
        ).values_list('user2', flat=True)
        return Response(friend_ids)


class SendMessageView(APIView):
    def post(self, request, *args, **kwargs):
        user_id = kwargs['user_id']
        message = request.data.get('message')

        if not message:
            return Response({'error': 'Message is required.'}, status=400)

        sender_id = request.user.id
        recipient_id = user_id

        sender = get_object_or_404(User, id=sender_id)
        recipient = get_object_or_404(User, id=recipient_id)

        is_friends_with = Friendship.objects.filter(
            Q(user1=sender, user2=recipient) | Q(user1=recipient, user2=sender)
        ).exists()

        if is_friends_with:
            serializer = MessageSerializer(data={
                'sender': sender_id,
                'recipient': recipient_id,
                'content': message
            })

            if serializer.is_valid():
                serializer.save()
                return Response({'success': True})
            else:
                return Response(serializer.errors, status=400)
        else:
            return Response({'error': 'You can only send messages to your friends.'}, status=403)
