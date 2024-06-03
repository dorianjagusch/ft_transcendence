# pong/consumers.py
import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from .game_status import PongStatus
from .constants import *

class PongConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = PongStatus()

    async def connect(self):
        await self.accept()
        # Start sending positions immediately after connection is established
        asyncio.create_task(self.send_positions_loop())

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        key_press = text_data.strip()
        self.game.update_positions(key_press)      
        if self.game.game_over == True:
            await self.send_positions()
            await self.close()
        await self.send_positions()


    async def send_positions(self):
        game_state = self.game.get_game_state()
        await self.send(text_data=json.dumps(game_state))

    async def send_consts(self):
        game_consts = self.game.get_consts()
        await self.send(text_data=json.dumps(game_consts))

    async def send_positions_loop(self):
        await self.send_consts()
        while True:
            self.game.update_ball_position()
            await self.send_positions()
            await asyncio.sleep(MESSAGE_INTERVAL_SECONDS)   # Wait for the specified interval before sending the next message
            if self.game.game_over == True:
                break
