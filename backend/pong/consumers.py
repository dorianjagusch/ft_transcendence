# pong/consumers.py
import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from .game_logic import PongGame
from .constants import *

from channels.db import database_sync_to_async
from Tokens.models import AuthenticatedGuestUserToken
from Match.models import Match
from Player.models import Player

class PongConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = PongGame()
        self.match = None
        self.player_one = None
        self.player_two = None

    async def connect(self):
        # Extract the match id and the token from the URL query string
        match_id = self.scope['url_route']['kwargs']['match_id']
        query_string = self.scope['query_string'].decode('utf-8')
        token = query_string.split('=')[1] if 'token=' in query_string else None

        result = await self.authenticate_and_fetch(token, match_id)
        if not result:
            await self.close()
            return

        # Authenticate token and fetch match and players
        await self.accept()
        # Start sending positions immediately after connection is established
        asyncio.create_task(self.send_positions_loop())

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # Receive key press messages from the client
        key_press = text_data.strip()
        # Update player positions based on key press
        self.game.update_positions(key_press)
        # Check if the game is over and disconnect if it is       
        if self.game.game_over == True:
            await self.send_positions()

            # SSALMI save the scores here, but how?

            await self.close()
        
        # Send updated positions to client
        await self.send_positions()


    async def send_positions(self):
        # Send positions to clients
        game_state = self.game.get_game_state()
        await self.send(text_data=json.dumps(game_state))  # Example of sending game state to client

    async def send_positions_loop(self):
        while True:
            self.game.update_ball_position()  # Update ball position
            await self.send_positions()  # Send positions to the client
            await asyncio.sleep(MESSAGE_INTERVAL_SECONDS)   # Wait for the specified interval before sending the next message
            if self.game.game_over == True:
                break
    
    @database_sync_to_async
    def authenticate_and_fetch(self, token, match_id):
        try:
            guest_token = AuthenticatedGuestUserToken.objects.get(token=token)
            if not token.is_active or token.is_expired():
                return False
            
            guest_token.is_active = False
            guest_token.save()

            self.match = Match.objects.get(id=match_id)
            self.player_one = Player.objects.get(match=self.match, user_id=guest_token.host_user)
            self.player_two = Player.objects.get(match=self.match, user_id=guest_token.guest_user)

            return True
            
        except (AuthenticatedGuestUserToken.DoesNotExist, Match.DoesNotExist, Player.DoesNotExist):
            return False
    
    @database_sync_to_async
    def save_match_final_results(self):
        # Save scores when the game is over
        self.player_one.score = self.game.player_one_score
        self.player_two.score = self.game.player_two_score

        # Determine and save the winner
        if self.game.player_one_score > self.game.player_two_score:
            self.player_one.match_winner = True
        else:
            self.player_two.match_winner = True

        self.player_one.save()
        self.player_two.save()
