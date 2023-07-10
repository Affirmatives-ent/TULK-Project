from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from chat.serializers import MessageSerializer
from django.shortcuts import get_object_or_404
from accounts.models import Friendship
from django.db.models import Q
from .models import Message

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.user = await self.get_user(self.user_id)

        if not self.user:
            await self.close()
        else:
            await self.channel_layer.group_add(
                f'chat_{self.user_id}',
                self.channel_name
            )

            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f'chat_{self.user_id}',
            self.channel_name
        )

    async def receive(self, text_data):
        sender_id, recipient_id, message = text_data.split(';')
        sender = await self.get_user(int(sender_id))
        recipient = await self.get_user(int(recipient_id))

        if sender and recipient:
            is_friends_with = await self.check_friends(sender, recipient)

            if is_friends_with:
                await self.save_message(sender, recipient, message)
                serializer = MessageSerializer(data={
                    'sender': sender_id,
                    'recipient': recipient_id,
                    'content': message
                })

                if serializer.is_valid():
                    serialized_message = serializer.data
                    await self.channel_layer.group_send(
                        f'chat_{recipient.id}',
                        {
                            'type': 'chat_message',
                            'message': serialized_message
                        }
                    )
                else:
                    await self.send(text_data='Invalid message data.')
            else:
                await self.send(text_data='You can only send messages to your friends.')
        else:
            await self.send(text_data='Invalid users.')

    @sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    @sync_to_async
    def check_friends(self, user1, user2):
        friendship_exists = Friendship.objects.filter(
            (Q(user1=user1, user2=user2) | Q(user1=user2, user2=user1))
        ).exists()
        return friendship_exists

    @sync_to_async
    def save_message(self, sender, recipient, message):
        Message.objects.create(
            sender=sender, recipient=recipient, content=message)
