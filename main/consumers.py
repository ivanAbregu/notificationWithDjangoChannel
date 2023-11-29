from asgiref.sync import async_to_sync
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

########################### FOR NOTIFCATION #######################

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            self.group_name = f"user_{self.scope['user'].id}"
            
            await self.channel_layer.group_add(self.group_name, self.channel_name)

            await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await self.channel_layer.group_send(
            self.group_name, {"type": "send_message", "message": message}
        )


    async def send_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))


def send_notification_to_customer(user_id, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
            f"user_{user_id}",
            {
                "type": "send_message",
                "message": message
            },
        )
