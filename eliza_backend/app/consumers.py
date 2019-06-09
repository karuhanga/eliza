from channels.generic.websocket import WebsocketConsumer
import json


consumer = None


class SpeechConsumer(WebsocketConsumer):
    def connect(self):
        global consumer
        consumer = self
        self.accept()

    def disconnect(self, close_code):
        global consumer
        consumer = None

    # Receive message from room group
    def chat_message(self, message, errored):

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'errored': errored,
        }))


def send_message(message, errored):
    if consumer:
        consumer.chat_message(message, errored)
    else:
        print('consumer is not set')
