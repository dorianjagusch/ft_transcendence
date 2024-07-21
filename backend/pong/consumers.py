# pong/consumers.py
from django.db import transaction
import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from .game import PongStatus
from .constants import *
from channels.db import database_sync_to_async
from Tokens.models import MatchToken
from Match.models import Match
from Match.matchState import MatchState
from Player.models import Player
from .pongPlayer import PongPlayer
from .ball import Ball
from Tournament.models import Tournament, TournamentPlayer
from Tournament.managers import TournamentManager


class PongConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.match = None
        self.player_left = PongPlayer(WALL_MARGIN)
        self.player_right = PongPlayer(PLAYGROUND_WIDTH - WALL_MARGIN)
        self.ai_opponent = False
        self.ai_target_y = self.player_right.y
        self.ball = Ball()
        self.game = PongStatus(self.ball, self.player_left, self.player_right)

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
                asyncio.create_task(self.ai_move_loop())
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

        await self.save_match_results()
        await self.close()

    @database_sync_to_async
    def authenticate_match_token_and_fetch_match_and_players(self, token, match_id):
        try:
            with transaction.atomic():
                match_token = MatchToken.objects.get(token=token)
                if not match_token.is_active or match_token.is_expired():
                    return False

                match_token.is_active = False
                match_token.save()

                self.match = Match.objects.get(pk=match_id)
                players = Player.objects.filter(match=self.match).order_by('id')
                if players.count() != 2:
                    return False
                self.player_left = players[0]
                self.player_right = players[1]

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
    def save_match_results(self):
        print("save_match_results", file=sys.stderr)
        self.match.state = MatchState.FINISHED

        # Save scores when the game is over
        self.player_left.score = self.game.player_left.score
        self.player_right.score = self.game.player_right.score

        # Determine and save the winner
        if self.game.player_left.score > self.game.player_right.score:
            self.player_left.match_winner = True
        else:
            self.player_right.match_winner = True

        try:
            with transaction.atomic():
                self.match.save()
                self.player_left.save()
                self.player_right.save()

                if self.match.tournament:
                    self.update_tournament_data_with_match_results(self.match)

        except Exception as e:
            self.abort_match(self.match)

    # @database_sync_to_async
    def update_tournament_data_with_match_results(self, match: Match):
        try:
            if not match.tournament:
                return

            winning_player = match.players.filter(match_winner=True).first()

            # this shouldn't happen, but in case, abort tournament
            if not winning_player:
                TournamentManager.in_progress.abort_tournament(match.tournament)

            with transaction.atomic():

                winning_tournament_player = TournamentPlayer.objects.get(
                    tournament=match.tournament,
                    user=winning_player.user
                )

                match.tournament.next_match += 1
                match.tournament.save()

                TournamentManager.in_progress.update_tournament_with_winning_tournament_player(winning_tournament_player)

        except Exception as e:
            print(f"An error occurred while updating match results: {e}", file=sys.stderr)

    @database_sync_to_async
    def start_match(self, match):
        match.start_match()

    @database_sync_to_async
    def abort_match(self, match: Match):
        match.abort_match()
        if match.tournament:
            TournamentManager.in_progress.abort_tournament(match.tournament)
