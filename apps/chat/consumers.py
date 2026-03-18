import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatThread, Message

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.thread_id = self.scope['url_route']['kwargs']['thread_id']
        self.room_group_name = f'chat_{self.thread_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message_text = text_data_json['message']
            user_id = self.scope['user'].id

            if not user_id:
                print("No user ID found in scope")
                return

            # Save message to database
            saved_msg = await self.save_message(user_id, self.thread_id, message_text)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message_text,
                    'sender_id': user_id,
                    'sender_name': self.scope['user'].full_name,
                    'created_at': saved_msg.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                }
            )
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Error in Consumer Receive: {e}")

    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender_id': event['sender_id'],
            'sender_name': event['sender_name'],
            'created_at': event['created_at'],
        }))

    @database_sync_to_async
    def save_message(self, user_id, thread_id, text):
        user = User.objects.get(id=user_id)
        thread = ChatThread.objects.get(id=thread_id)
        return Message.objects.create(sender=user, thread=thread, text=text)
