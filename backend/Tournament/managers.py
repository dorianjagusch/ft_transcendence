from django.db import models, transaction, IntegrityError
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.utils import timezone
from .models import Tournament, \
                          TournamentPlayer, \
                            TournamentState
from .exceptions import TournamentCreationException, \
                              TournamentInProgressException
from .tournamentMacros import TOURNAMENT_EXPIRERY_TIME_SECONDS
from Match.models import Match
from User.models import User
from Player.models import Player

import sys


class TournamentSetupManager:
    @staticmethod
    def create_tournament_and_its_participants(tournament_creation_serializer_validated_data):
        try:
            with transaction.atomic():

                tournament = Tournament.objects.create(
                    host_user = tournament_creation_serializer_validated_data['host_user'],
                    custom_name = tournament_creation_serializer_validated_data.get('custom_name', None),
                    player_amount = len(tournament_creation_serializer_validated_data['tokens']) + 1
                )

                if tournament_creation_serializer_validated_data.get('host_user_custom_name', None):
                    host_name_in_tournament = tournament_creation_serializer_validated_data['host_user_custom_name']
                else:
                    host_name_in_tournament = tournament_creation_serializer_validated_data['host_user'].username
                TournamentPlayer.objects.create(
                    tournament=tournament,
                    user=tournament.host_user,
                    name_in_tournament=host_name_in_tournament
                )

                for token_data in tournament_creation_serializer_validated_data['tokens']:
                    guest_name_in_tournament = token_data.custom_name if token_data.custom_name else token_data.guest_user.username
                    TournamentPlayer.objects.create(
                        tournament=tournament,
                        user=token_data.guest_user,
                        name_in_tournament=guest_name_in_tournament
                    )

                TournamentSetupManager.setup_tournament_matches(tournament)
                return tournament.id
                
        except Exception as e:
            raise TournamentCreationException(f"An error occurred while creating tournament and its participants: {e}")


    @staticmethod
    def setup_tournament_matches(tournament: Tournament):        
        if tournament.state != TournamentState.IN_PROGRESS or tournament.next_match != 0:
            raise TournamentInProgressException("Tournament is not in a valid state to set up matchups.")
        
        tournament_players = list(tournament.players.all())
        if len(tournament_players) != tournament.player_amount:
            raise TournamentInProgressException("The number of tournament_players does not match the expected player amount.")
        
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

                # CREATE THE REST OF THE TOURNAMENT MATCHES
                # THE MATCH WINNERS WILL BE ASSIGNED TO THEM LATER ON
                for tournament_match_id in range(len(tournament_players) // 2, match_amount):
                    Match.objects.create(
                        tournament=tournament,
                        tournament_match_id=tournament_match_id
                    )
                    
                TournamentSetupManager.start_tournament(tournament)

        except Exception as e:
            raise TournamentInProgressException(f"An error occurred while setting up matchups: {e}")

    @staticmethod
    def start_tournament(tournament: Tournament):
        tournament.start_ts = timezone.now()
        tournament.expires_ts = tournament.start_ts + timedelta(seconds=TOURNAMENT_EXPIRERY_TIME_SECONDS)
        tournament.save()

class TournamentInProgressManager:
    @staticmethod
    def make_sure_active_tournament_is_still_valid(tournament: Tournament) -> None:
        if timezone.now() > tournament.expires_ts:
            tournament.abort_tournament()
            raise TournamentInProgressException(f"Tournament not finished in time; tournament aborted")
        TournamentInProgressManager.make_sure_users_in_active_tournament_are_still_active(tournament)

    @staticmethod
    def make_sure_users_in_active_tournament_are_still_active(tournament: Tournament) -> None:       
        tournament_players = TournamentPlayer.objects.filter(tournament=tournament)
        inactive_users = tournament_players.filter(user__is_active=False)
        if inactive_users.exists():
            raise TournamentInProgressException(f"An user in the tournament has deleted their account; tournament aborted")

    @staticmethod
    def assign_winner_to_next_tournament_match_with_less_than_two_players(winner: User) -> None:
        try:
            with transaction.atomic():
                tournament = winner.tournament
                try:
                    coming_tournament_matches = Match.objects.filter(
                        tournament=tournament,
                        tournament_match_id__gte=tournament.next_match
                    ).order_by('tournament_match_id')

                except Match.DoesNotExist:
                    raise TournamentInProgressException("No future matchup with empty player slot")
                
                for match in coming_tournament_matches:
                    if len(Player.objects.filter(match=match)) < 2:
                        Player.objects.create(
                            user=winner,
                            match=match
                        )
                        return

                # something went wrong if we got here
                raise TournamentInProgressException("No future matchup with empty participant slot")

        except Exception as e:
            raise TournamentInProgressException(f"An error occurred while assigning the match winner to future match: {e}")
        
    @staticmethod
    def update_tournament_with_winning_tournament_player(winning_tournament_player: TournamentPlayer) -> None:
        try:
            with transaction.atomic():
                tournament = winning_tournament_player.tournament
                next_tournament_match_id = tournament.next_match
                
                # check if there is a next match in the tournament.
                # if there is a next match, create a player from the winning_tournament_player.user for next tournament match with less than two players
                # if no next match, set user as tournament winner and finish tournament
                try:
                    Match.objects.get(
                        tournament=tournament,
                        tournament_match_id=next_tournament_match_id
                    )
                    TournamentInProgressManager.assign_winner_to_next_tournament_match_with_less_than_two_players(winning_tournament_player.user)

                except Match.DoesNotExist:
                    tournament.winner = winning_tournament_player.user
                    tournament.state = TournamentState.FINISHED
                    tournament.save()

        except Exception as e:
            raise TournamentInProgressException(f"An error occurred while updating tournament data after finished match: {e}")
        
    @staticmethod
    def abort_tournament(tournament: Tournament):
        tournament.abort_tournament()
        Match.objects.abort_tournament_matches(tournament.pk)



        
