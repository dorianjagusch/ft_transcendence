# pong/consumers.py
import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer

# Define constants for player movement and playground size
PLAYER_MOVEMENT_UNIT = 1
PLAYGROUND_WIDTH = 1000
PLAYGROUND_HEIGHT = 400
MESSAGE_INTERVAL_SECONDS = 0.05  # 50 milliseconds

class PongConsumer(AsyncWebsocketConsumer):
    player1_y = PLAYGROUND_HEIGHT // 2  # Initial position for player 1
    player2_y = PLAYGROUND_HEIGHT // 2  # Initial position for player 2
    ball_x = PLAYGROUND_WIDTH // 2      # Initial position for ball (x-coordinate)
    ball_y = PLAYGROUND_HEIGHT // 2     # Initial position for ball (y-coordinate)

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
        if key_press == 'w':
            self.player1_y -= PLAYER_MOVEMENT_UNIT  # Move player 1 up
        elif key_press == 's':
            self.player1_y += PLAYER_MOVEMENT_UNIT  # Move player 1 down
        elif key_press == 'o':
            self.player2_y -= PLAYER_MOVEMENT_UNIT  # Move player 2 up
        elif key_press == 'l':
            self.player2_y += PLAYER_MOVEMENT_UNIT  # Move player 2 down
        
        # Ensure player positions stay within the bounds of the play area
        self.player1_y = max(min(self.player1_y, PLAYGROUND_HEIGHT - 40), 0)  # Bound player 1 between 0 and (playground height - player height)
        self.player2_y = max(min(self.player2_y, PLAYGROUND_HEIGHT - 40), 0)  # Bound player 2 between 0 and (playground height - player height)
        
        # Send updated player and ball positions to the client
        await self.send_positions()

    async def send_positions(self):
        # Construct JSON message with player and ball positions
        message = {
            'player1_y': self.player1_y,
            'player2_y': self.player2_y,
            'ball_x': self.ball_x,
            'ball_y': self.ball_y,
        }
        # Send JSON message to the client
        await self.send(text_data=json.dumps(message))

    async def send_positions_loop(self):
        while True:
            await self.send_positions()  # Send positions to the client
            await asyncio.sleep(MESSAGE_INTERVAL_SECONDS)   # Wait for the specified interval before sending the next message
