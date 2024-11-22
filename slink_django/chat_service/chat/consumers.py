import json
from uuid import UUID

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.models import Chat, Message, MessageImage


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # chat = chat_id
        # group = chat_{chat_id}
        self.chat_id = self.scope["url_route"]["kwargs"]["chat"]
        self.group = f'chat_{self.chat_id}'

        # Присоединяемся к группе
        await self.channel_layer.group_add(
            self.group,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Отключаемся от группы
        await self.channel_layer.group_discard(
            self.group,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        user = data.get("user")
        text = data.get("text")
        images = data.get("images", [])

        try:
            chat = self.get_chat(self.chat_id)

            message = self.create_message(user, chat, text)

            self.create_message_image(message, images)

            response = {
                "user": user,
                "text": text,
                "created_at": message.created_at.isoformat(),
                "images": images,
            }

            await self.channel_layer.group_send(
                self.group,
                {
                    "type": "chat_message",
                    "message": response,
                }
            )

        except Chat.DoesNotExist:
            await self.send(text_data=json.dumps({"error": "Чат не найден"}))

    async def chat_message(self, event):
        message = event["message"]

        await self.send(text_data=json.dumps(message))

    @database_sync_to_async
    def get_chat(self, chat_id):
        return Chat.objects.get(id=chat_id)

    @database_sync_to_async
    def create_message(self, user, chat, text):
        return Message.objects.create(
            user=user,
            chat=chat,
            text=text,
        )

    @database_sync_to_async
    def create_message_image(self, message, images):
        for image in images:
            MessageImage.objects.create(message=message, image=image)