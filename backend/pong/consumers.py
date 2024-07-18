# pong/consumers.py
import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from .game import PongStatus
from .constants import *

from channels.db import database_sync_to_async
from Tokens.models import MatchToken
from Match.models import Match
from Player.models import Player
import sys

class PongConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.match = None
        self.player_left = None
        self.player_right = None
        self.ai_opponent = True
        self.game = PongStatus()

    async def connect(self):
        # Extract the match id and the token from the URL query string
        match_id = self.scope['url_route']['kwargs']['match_id']
        query_string = self.scope['query_string'].decode('utf-8')
        token = query_string.split('=')[1] if 'token=' in query_string else None

        authenticated = await self.authenticate_match_token_and_fetch_match_and_players(token, match_id)
        if authenticated:
            if self.ai_opponent is True:
                self.game.use_ai_opponent()
                asyncio.create_task(self.ai_opponent_loop())
            self.start_match(self.match)
            await self.accept()
            asyncio.create_task(self.send_positions_loop())
        else:
            await self.close()
            return

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        key_press = text_data.strip()
        self.game.update_positions(key_press)

        if self.game.game_stats.game_over == True:
            await self.send_positions()
            await self.save_match_final_results()
            await self.close()

        await self.send_positions()

    async def ai_opponent_loop(self):
        while not self.game.game_stats.game_over:
            self.game.ai_move_paddle()
            await asyncio.sleep(1)

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
            await asyncio.sleep(MESSAGE_INTERVAL_SECONDS)
            if self.game.game_stats.game_over == True:
                break

        await self.save_match_final_results()
        await self.close()

    @database_sync_to_async
    def authenticate_match_token_and_fetch_match_and_players(self, token, match_id):
        try:
            match_token = MatchToken.objects.get(token=token)
            if not match_token.is_active or match_token.is_expired():
                return False

            match_token.is_active = False
            match_token.save()

            self.match = Match.objects.get(pk=match_id)
            self.player_left = Player.objects.filter(match=self.match, user_id=match_token.user_left_side).first()
            if match_token.user_right_side is not None:
                self.player_right = Player.objects.filter(match=self.match, user_id=match_token.user_right_side).first()
            else:
                self.ai_opponent = True
            return True
        except (MatchToken.DoesNotExist, Match.DoesNotExist, Player.DoesNotExist):
            return False

    @database_sync_to_async
    def save_match_final_results(self):
        self.player_left.score = self.game.player_left.score
        self.player_right.score = self.game.player_right.score

        if self.game.player_left.score > self.game.player_right.score:
            self.player_left.match_winner = True
        else:
            self.player_right.match_winner = True

        self.player_left.save()
        self.player_right.save()

    @database_sync_to_async
    def start_match(self, match):
        match.start_match()
