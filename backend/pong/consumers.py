# pong/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class PongConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        message = json.loads(text_data)['message']
        key = message.strip()
        response_data = {}

        if key == 's':
            response_data['message'] = 'S key pressed'
        elif key == 'w':
            response_data['message'] = 'W key pressed'
        elif key == 'l':
            response_data['message'] = 'L key pressed'
        elif key == 'o':
            response_data['message'] = 'O key pressed'
        else:
            response_data['message'] = 'Invalid key'

        # Send JSON response
        await self.send(text_data=json.dumps(response_data))
