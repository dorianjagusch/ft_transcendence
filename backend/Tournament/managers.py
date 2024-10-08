from django.db import transaction
from django.utils import timezone
from datetime import timedelta

from .models import Tournament, TournamentPlayer
from .serializers import TournamentCreationSerializer
from .exceptions import TournamentSetupException, TournamentInProgressException
from .tournamentState import TournamentState
from .tournamentMacros import TOURNAMENT_EXPIRY_TIME_SECONDS
from User.models import User
from Match.models import Match
from Match.matchState import MatchState
from Player.models import Player

class TournamentManager:
    @staticmethod
    def create_tournament_and_tournament_player_for_host(validated_data: TournamentCreationSerializer.validated_data):
        try:
            with transaction.atomic():
                tournament = Tournament.objects.create(
                    name=validated_data.get('name', None),
                    host_user=validated_data['host_user'],
                    player_amount=validated_data['player_amount'],
                    expire_ts=timezone.now() + timedelta(TOURNAMENT_EXPIRY_TIME_SECONDS),
                )

                display_name = validated_data.get('host_user_display_name', None)
                username = tournament.host_user.username
                try:
                    TournamentManager.create_tournament_player(tournament, tournament.host_user, display_name or username)
                except Exception as e:
                    tournament.delete()
                    raise Exception(e)

                return tournament

        except Exception as e:
            raise TournamentSetupException(e)

    @staticmethod
    def setup_tournament_matches(tournament: Tournament) -> None:
        if tournament.state != TournamentState.LOBBY or tournament.next_match != 0:
            raise TournamentSetupException("Tournament is not in a valid state to set up matchups.")

        tournament_players = list(tournament.players.all())
        if len(tournament_players) != tournament.player_amount:
            raise TournamentSetupException("The number of tournament_players does not match the expected player amount.")

        match_amount = tournament.player_amount - 1
        if match_amount not in [3, 7]:
            raise TournamentSetupException("Match amount can only be 3 or 7.")

        try:
            with transaction.atomic():

                # assignment of players to initial matches are done based on the order of the TournamentPlayers
                # if you want to set the players for the initial matches based on some other algorithm, replace this part
                for i in range(0, len(tournament_players), 2):
                    match = Match.objects.create(
                        tournament=tournament
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
                for unfilled_matches in range(len(tournament_players) // 2, match_amount):
                    Match.objects.create(
                        tournament=tournament
                    )

        except Exception as e:
            raise TournamentSetupException(f"An error occurred while setting up matchups: {e}")

    @staticmethod
    def start_tournament(tournament: Tournament) -> TournamentCreationSerializer:
        player_amount = tournament.players.count()
        if player_amount != tournament.player_amount:
            raise TournamentSetupException(f"Tournament must have {tournament.player_amount} players to start, but currently it has {player_amount} players.")
        TournamentManager.setup_tournament_matches(tournament)
        tournament.start_tournament()
        tournament.save()


    @staticmethod
    def raise_error_if_tournament_has_expired(tournament: Tournament) -> None:
        if timezone.now() > tournament.expire_ts:
            raise TournamentInProgressException(f"Tournament not finished in time")

    @staticmethod
    def raise_error_if_inactive_user_in_tournament(tournament: Tournament) -> None:
        tournament_players = TournamentPlayer.objects.filter(tournament=tournament)
        inactive_users = tournament_players.filter(user__is_active=False)
        if inactive_users.exists():
            raise TournamentInProgressException(f"A user in the unfinished tournament has deleted their account")

    @staticmethod
    def update_tournament_with_winning_tournament_player(winning_tournament_player: TournamentPlayer) -> None:
        try:
            with transaction.atomic():
                tournament = winning_tournament_player.tournament

                # if no next match, set user as tournament winner and finish tournament
                if tournament.next_match >= tournament.matches.count():
                    tournament.winner = winning_tournament_player.user
                    tournament.state = TournamentState.FINISHED
                    tournament.save()
                else:
                    # if there is a next match, create a player from the winning_tournament_player.user for next tournament match with less than two players
                    TournamentManager.assign_winner_to_next_tournament_match_with_less_than_two_players(winning_tournament_player)


        except Exception as e:
            raise TournamentInProgressException(f"An error occurred while updating tournament data after finished match: {e}")

    @staticmethod
    def assign_winner_to_next_tournament_match_with_less_than_two_players(winning_tournament_player: TournamentPlayer) -> None:
        try:
            with transaction.atomic():
                tournament = winning_tournament_player.tournament
                try:
                    tournament_matches = Match.objects.filter(
                        tournament=tournament
                    ).order_by('id')

                except Match.DoesNotExist:
                    raise TournamentInProgressException("No future matchup with empty player slot")

                for match in tournament_matches:
                    if len(Player.objects.filter(match=match)) < 2:
                        Player.objects.create(
                            user=winning_tournament_player.user,
                            match=match
                        )
                        return

                # something went wrong if we got here
                raise TournamentInProgressException("No future tournament match with empty players")

        except Exception as e:
            raise TournamentInProgressException(f"An error occurred while assigning the match winner to future match: {e}")


    @staticmethod
    def abort_tournament(tournament: Tournament) -> None:
        tournament.abort_tournament()
        TournamentManager.abort_tournament_matches(tournament)

    @staticmethod
    def abort_tournament_matches(tournament: Tournament):
        tournament_matches = Match.objects.filter(
            tournament=tournament
        ).order_by('id')

        for match in tournament_matches:
            if match.state in [MatchState.LOBBY, MatchState.IN_PROGRESS]:
                match.state = MatchState.ABORTED
                match.save()

    @staticmethod
    def create_tournament_player(tournament: Tournament, user: User, display_name: str | None) -> TournamentPlayer:
        tournament_player = TournamentPlayer.objects.create(
                    tournament=tournament,
                    user=user,
                    display_name=display_name
                )
        return tournament_player
