from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

class PriceConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'example_room_name'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive price from WebSocket
    def receive(self, text_data):
        price_data_json = json.loads(text_data)
        price = price_data_json['price']

        # Send price to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_price', # this method is defined below
                'price': price
            }
        )

    # Receive message from room group
    def send_price(self, event):
        price = event['price']

        # Send price to WebSocket
        self.send(text_data=json.dumps({
            'price': 'a price'
        }))