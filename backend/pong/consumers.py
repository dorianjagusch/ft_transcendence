# pong/consumers.py
import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from .game_logic import PongGame
from .constants import *

class PongConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = PongGame()

    async def connect(self):
        await self.accept()
        # Start sending positions immediately after connection is established
        asyncio.create_task(self.send_positions_loop())

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # Receive key press messages from the client
        key_press = text_data.strip()
        # Update player positions based on key press
        self.game.update_player_positions(key_press)
        # Send updated positions to client
        await self.send_positions()

    async def send_positions(self):
        # Send positions to clients
        game_state = self.game.get_game_state()
        await self.send(text_data=json.dumps(game_state))  # Example of sending game state to client

    async def send_positions_loop(self):
        while True:
            await self.send_positions()  # Send positions to the client
            await asyncio.sleep(MESSAGE_INTERVAL_SECONDS)   # Wait for the specified interval before sending the next message
