# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Friendship


class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Implement WebSocket connection and authentication logic
        await self.accept()

        # Get the authenticated user and set them as online
        user = await self.get_user_from_context()
        await self.set_user_online(user)

    async def disconnect(self, close_code):
        # Handle WebSocket disconnection
        user = await self.get_user_from_context()
        await self.set_user_offline(user)

    async def receive(self, text_data):
        # Implement WebSocket messages handling (if needed)
        pass

    async def send_online_status(self, event):
        # Broadcast online status to the relevant users
        await self.send(text_data=json.dumps({
            'type': 'online_status',
            'user_id': event['user_id'],
            'is_online': event['is_online'],
        }))

    @database_sync_to_async
    def get_user_from_context(self):
        # Get the authenticated user from the WebSocket scope
        user_id = self.scope['user'].id
        return User.objects.get(id=user_id)

    @database_sync_to_async
    def set_user_online(self, user):
        # Update user's online status in the database and broadcast it
        user.is_online = True
        user.save()
        self.send_online_status({'user_id': user.id, 'is_online': True})

    @database_sync_to_async
    def set_user_offline(self, user):
        # Update user's online status in the database and broadcast it
        user.is_online = False
        user.save()
        self.send_online_status({'user_id': user.id, 'is_online': False})
