from django.db import transaction
from datetime import timezone, timedelta

from .models import Tournament, \
                        TournamentPlayer
from .serializers import TournamentCreationSerializer
from .exceptions import TournamentSetupException
from .tournamentState import TournamentState
from .tournamentMacros import TOURNAMENT_EXPIRY_TIME_SECONDS
from User.models import User
from Match.models import Match
from Match.matchState import MatchState
from Player.models import Player

class TournamentSetupManager:
    @staticmethod
    def create_tournament_and_tournament_player_for_host(validated_data: TournamentCreationSerializer.validated_data):
        try:
            with transaction.atomic():
                tournament = Tournament.objects.create(
                    name=validated_data['name'] if validated_data['name'] else None,
                    host_user=validated_data['host_user'],
                    player_amount=validated_data['player_amount'],
                    expires_ts=timezone.now() + timedelta(TOURNAMENT_EXPIRY_TIME_SECONDS),
                )

                TournamentPlayer.objects.create(
                    tournament=tournament,
                    user=tournament.host_user,
                    display_name=validated_data['host_user_display_name'] if validated_data['host_user_display_name'] else None,
                )

                return tournament

        except Exception as e:
            return TournamentSetupException(e)

    @staticmethod
    def setup_tournament_matches(tournament: Tournament) -> None:        
        if tournament.state != TournamentState.IN_PROGRESS or tournament.next_match != 0:
            raise TournamentSetupException("Tournament is not in a valid state to set up matchups.")
        
        tournament_players = list(tournament.players.all())
        if len(tournament_players) != tournament.player_amount:
            raise TournamentSetupException("The number of tournament_players does not match the expected player amount.")
        
        match_amount = tournament.player_amount - 1

        try:
            with transaction.atomic():

                # assignement of players to initial matches are done based on the order of the TournamentPlayers
                # if you want to set the players for the initial matches based on some other algorithm, replace this part
                for i in range(0, len(tournament_players), 2):
                    match = Match.objects.create(
                        tournament=tournament,
                        tournament_match_id=i // 2
                    )
                    Player.objects.create(
                        user=tournament_players[i].user,
                        match=match
                    )
                    Player.objects.create(
                        user=tournament_players[i+1].user,
                        match=match
                    )               

                # create the rest of the tournament matches
                # the match winners will be assigned to them later
                for tournament_match_id in range(len(tournament_players) // 2, match_amount):
                    Match.objects.create(
                        tournament=tournament,
                        tournament_match_id=tournament_match_id
                    )

        except Exception as e:
            raise TournamentSetupException(f"An error occurred while setting up matchups: {e}")

    @staticmethod
    def start_tournament(tournament: Tournament) -> TournamentCreationSerializer:
        player_amount = tournament.players.count()
        if player_amount != tournament.player_amount:
            raise TournamentSetupException(f"tournament must have {tournament.player_amount} players to start, but currently it has {player_amount} players.")
        TournamentInProgressManager.setup_tournament_matches(tournament)
        tournament.start_ts = timezone.now()
        tournament.save()

class TournamentInProgressManager:
    @staticmethod
    def abort_tournament(tournament: Tournament) -> None:
        tournament.abort_tournament()
        Match.objects.abort_tournament_matches(tournament)

    @staticmethod
    def abort_tournament_matches(tournament: Tournament):
        tournament_matches = Match.objects.filter(
            tournament=tournament
        ).order_by('tournament_match_id')

        for match in tournament_matches:
            if match.state in [MatchState.LOBBY, MatchState.IN_PROGRESS]:
                match.state = MatchState.ABORTED
                match.save()