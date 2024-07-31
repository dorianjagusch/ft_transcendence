# pong/consumers.py
from django.db import transaction
import json
import asyncio
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .game import PongStatus
from .constants import *
from channels.db import database_sync_to_async
from Tokens.models import MatchToken
from Match.models import Match
from Match.matchState import MatchState
from Player.models import Player
from Tournament.models import Tournament, TournamentPlayer
from Tournament.managers import TournamentManager
from .pongPlayer import PongPlayer
from .ball import Ball
from django.utils import timezone

class PongConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.match = None
        self.player_left = PongPlayer(WALL_MARGIN)
        self.left_name = None
        self.player_right = PongPlayer(PLAYGROUND_WIDTH - WALL_MARGIN)
        self.right_name = None
        self.ai_opponent = False
        self.ai_target_y = self.player_right.y
        self.ball = Ball()
        self.ball_contacts = 0
        self.ball_max_speed = BALL_SPEED
        self.game = PongStatus(self.ball, self.player_left, self.player_right, self.ball_contacts, self.ball_max_speed)
        self.match_ended_normally = False

    async def connect(self):
        # Extract the match id and the token from the URL query string
        match_id = self.scope['url_route']['kwargs']['match_id']
        query_string = self.scope['query_string'].decode('utf-8')
        token = query_string.split('=')[1] if 'token=' in query_string else None

        authenticated = await self.authenticate_match_token_and_fetch_match_and_players(token, match_id)
        if authenticated:
            await self.set_names(self.match)
            if self.ai_opponent is True:
                self.game.use_ai_opponent()
                asyncio.create_task(self.ai_opponent_loop())
                asyncio.create_task(self.ai_move_loop())

            self.match.start_time = timezone.now
            await self.start_match(self.match)
            await self.accept()
            asyncio.create_task(self.send_positions_loop())
        else:
            await self.close()
            return

    async def disconnect(self, close_code):
        if not self.match_ended_normally:
            await self.abort_match(self.match)

    async def receive(self, text_data):
        key_press = text_data.strip()
        self.game.update_positions(key_press)

        if self.game.game_stats.game_over == True:
            await self.send_positions()
            await self.save_match_results()
            await self.close()

        await self.send_positions()

    async def ai_move_loop(self):
        while not self.game.game_stats.game_over:
            await self.game.ai_move_paddle(self.ai_target_y)
            await asyncio.sleep(0.1)

    async def ai_opponent_loop(self):
        while not self.game.game_stats.game_over:
            self.ai_target_y = self.game.calculate_ai_steps()
            await asyncio.sleep(1)

    async def send_positions(self):
        game_state = self.game.get_game_state()
        await self.send(text_data=json.dumps(game_state))

    async def send_consts(self):
        game_consts = self.game.get_consts(self.left_name, self.right_name)
        await self.send(text_data=json.dumps(game_consts))

    async def send_positions_loop(self):
        await self.send_consts()
        while True:
            self.game.update_ball_position()
            await self.send_positions()
            await asyncio.sleep(MESSAGE_INTERVAL_SECONDS)
            if self.game.game_stats.game_over == True:
                self.match.end_time = timezone.now
                break

        await self.save_match_results()
        await self.close()

    @database_sync_to_async
    def authenticate_match_token_and_fetch_match_and_players(self, token, match_id):
        try:
            with transaction.atomic():
                match_token = MatchToken.objects.filter(token=token).first()
                if not match_token or not match_token.is_active or match_token.is_expired():
                    return False

                match_token.is_active = False
                match_token.save()

                self.match = Match.objects.filter(pk=match_id).first()
                if not self.match:
                    return False
                self.player_left = Player.objects.filter(match=self.match, user_id=match_token.user_left_side).first()
                if not self.player_left:
                    return False
                if match_token.user_right_side is not None:
                    self.player_right = Player.objects.filter(match=self.match, user_id=match_token.user_right_side).first()
                    if not self.player_right:
                        return False
                else:
                    self.ai_opponent = True
                return True

        except Exception:
            return False

    @database_sync_to_async
    def set_names(self, match: Match) -> None:
        if not match.tournament:
            self.left_name = self.player_left.user.username
            if not self.ai_opponent:
                self.right_name = self.player_right.user.username
            else:
                self.right_name = "AI"
        else:
            self.left_name = TournamentPlayer.objects.filter(tournament=self.match.tournament, user=self.player_left.user).first().display_name
            self.right_name = TournamentPlayer.objects.filter(tournament=self.match.tournament, user=self.player_right.user).first().display_name


    @database_sync_to_async
    def save_match_results(self):
        self.match.finish_match()
        ball_stats = self.game.get_ball_stats()
        self.match.ball_contacts = ball_stats['ball_contacts']
        self.match.ball_max_speed = ball_stats['ball_max_speed']

        # Save scores when the game is over
        self.player_left.score = self.game.player_left.score
        self.player_right.score = self.game.player_right.score

        # Determine and save the winner
        if self.game.player_left.score > self.game.player_right.score:
            self.player_left.match_winner = True
        else:
            self.player_right.match_winner = True

        try:
            self.match.save()
            self.player_left.save()
            if self.ai_opponent is False:
                self.player_right.save()

            if self.match.tournament:
                self.update_tournament_data_with_match_results(self.match)

            self.match_ended_normally = True

        except Exception as e:
            self.abort_match(self.match)

    def update_tournament_data_with_match_results(self, match: Match):
        try:
            if not match.tournament:
                return

            winning_player = match.players.filter(match_winner=True).first()

            # this shouldn't happen, but in case, abort tournament
            if not winning_player:
                TournamentManager.in_progress.abort_tournament(match.tournament)
                return

            winning_tournament_player = TournamentPlayer.objects.get(
                tournament=match.tournament,
                user=winning_player.user
            )

            match.tournament.next_match += 1
            match.tournament.save()

            TournamentManager.in_progress.update_tournament_with_winning_tournament_player(winning_tournament_player)

        except Exception as e:
            TournamentManager.in_progress.abort_tournament(match.tournament)

    async def start_match(self, match: Match):
        await sync_to_async(match.start_match)()

    @database_sync_to_async
    def abort_match(self, match: Match):
        match.abort_match()
        if match.tournament:
            TournamentManager.in_progress.abort_tournament(match.tournament)
