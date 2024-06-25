# pong/consumers.py
import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from .game import PongStatus
from .constants import *

from channels.db import database_sync_to_async
from django.db import transaction
from Tokens.models import MatchToken
from Match.models import Match
from Match.matchState import MatchState
from Player.models import Player
from Tournament.models import TournamentPlayer
from Tournament.managers import TournamentInProgressManager

import sys

class PongConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.match = None
        self.player_left = None
        self.player_right = None

        self.game = PongStatus()



    async def connect(self):
        # Extract the match id and the token from the URL query string
        match_id = self.scope['url_route']['kwargs']['match_id']
        query_string = self.scope['query_string'].decode('utf-8')
        token = query_string.split('=')[1] if 'token=' in query_string else None

        authenticated = await self.authenticate_match_token_and_fetch_match_and_players(token, match_id)
        if authenticated:
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
        #move = get_move(key_press)
        self.game.update_positions(key_press)      
        if self.game.game_stats.game_over == True:
            await self.send_positions()

            # save the final results of the match
            await self.save_match_results()

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
            if self.game.game_stats.game_over == True:
                break

        # save the final results of the match
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
                players = Player.objects.filter(match=self.match)
                if players.count() != 2:
                    return False
                self.player_left = players[0]
                self.player_right = players[1]

                return True
            
        except (MatchToken.DoesNotExist, Match.DoesNotExist, Player.DoesNotExist):
            return False

        
    @database_sync_to_async
    def start_match(self, match):
        match.start_match()

    @database_sync_to_async
    def abort_match(self, match: Match):
        match.abort_match()
        if match.tournament:
            TournamentInProgressManager.abort_tournament(match.tournament)

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
            print("bef", file=sys.stderr)
            with transaction.atomic():
                print("aft", file=sys.stderr)
                self.match.save()
                print("\t1", file=sys.stderr)
                self.player_left.save()
                print("\t2", file=sys.stderr)
                self.player_right.save()
                print("\t3", file=sys.stderr)

                print("bef self.update_tournament_data_with_match_results", file=sys.stderr)
                self.update_tournament_data_with_match_results(self.match)

        except Exception as e:
            self.abort_match(self.match)

    # @database_sync_to_async
    def update_tournament_data_with_match_results(self, match: Match):
        print("update_tournament_data_with_match_results", file=sys.stderr)
        try:
            print("update_tournament_data_with_match_results in TRY", file=sys.stderr)
            if not match.tournament:
                print("No tournament associated with this match", file=sys.stderr)
                return
            
            winning_player = match.players.filter(match_winner=True).first()

            # this shouldn't happen, but in case, abort tournament
            if not winning_player:
                print("No tournament match winner", file=sys.stderr)
                TournamentInProgressManager.abort_tournament(match.tournament)
            
            with transaction.atomic():
            
                winning_tournament_player = TournamentPlayer.objects.get(
                    tournament=match.tournament,
                    user=winning_player.user
                )

                match.tournament.next_match += 1
                match.tournament.save()

                print("before update_tournament_with_winning_tournament_player", file=sys.stderr)
                TournamentInProgressManager.update_tournament_with_winning_tournament_player(winning_tournament_player)
        
        except Exception as e:
            print(f"An error occurred while updating match results: {e}", file=sys.stderr)

            