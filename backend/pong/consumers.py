# pong/consumers.py
import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from .game_logic import PongGame
from .constants import *

from channels.db import database_sync_to_async
from Tokens.models import MatchToken
from Match.models import Match
from Player.models import Player

class PongConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = PongGame()
        self.match = None
        self.token = None
        self.player_left = None
        self.player_right = None

    async def connect(self):
        # Extract the match id and the token from the URL query string
        match_id = self.scope['url_route']['kwargs']['match_id']
        query_string = self.scope['query_string'].decode('utf-8')
        token = query_string.split('=')[1] if 'token=' in query_string else None

        self.token = await self.authenticate_match_token_and_fetch_match_and_players(token, match_id)
        if token:
            self.start_match(self.match)
            await self.accept()
            asyncio.create_task(self.send_positions_loop())
        else:
            await self.close()
            return

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

            # save the final results of the match
            await self.save_match_final_results()

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
    def authenticate_match_token_and_fetch_match_and_players(self, token, match_id):
        try:
            match_token = MatchToken.objects.get(token=token)
            if not token.is_active or token.is_expired():
                return None
            
            match_token.is_active = False
            match_token.save()

            self.match = Match.objects.get(pk=match_id)
            self.player_left = Player.objects.get(match=self.match, user_id=match_token.user_left_side)
            self.player_right = Player.objects.get(match=self.match, user_id=match_token.user_right_side)

            return match_token
            
        except (MatchToken.DoesNotExist, Match.DoesNotExist, Player.DoesNotExist):
            return None
    
    @database_sync_to_async
    def save_match_final_results(self):
        # Save scores when the game is over
        self.player_left.score = self.game.player_left_score
        self.player_right.score = self.game.player_right_score

        # Determine and save the winner
        if self.game.player_left_score > self.game.player_right_score:
            self.player_left.match_winner = True
        else:
            self.player_right.match_winner = True

        self.player_left.save()
        self.player_right.save()
        
    @database_sync_to_async
    def start_match(self, match):
        match.start_match()