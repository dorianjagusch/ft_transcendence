from django.db import models, transaction, IntegrityError
from django.core.exceptions import ValidationError
from datetime import datetime
from .models import Tournament, \
                          TournamentParticipant, \
                        TournamentMatchup, \
                        TournamentState
from .exceptions import TournamentCreationException, \
                              TournamentInProgressException
from Match.models import Match
from Tokens.models import TournamentGuestToken
from User.models import User
from Player.models import Player

import sys


class TournamentSetupManager:
    @staticmethod
    def create_tournament_and_its_participants(tournament_creation_serializer_validated_data):
        try:
            with transaction.atomic:

                tournament = Tournament.objects.create(
                    host_user = tournament_creation_serializer_validated_data['host_user'],
                    custom_name = tournament_creation_serializer_validated_data['custom_name'],
                    player_amount = len(tournament_creation_serializer_validated_data['tokens']) + 1
                )

                if tournament_creation_serializer_validated_data['host_user_custom_name'] is not None:
                    host_name_in_tournament = tournament_creation_serializer_validated_data['host_user_custom_name']
                else:
                    host_name_in_tournament = tournament_creation_serializer_validated_data['host_user'].username

                TournamentParticipant.objects.create(
                    tournament = tournament,
                    user = tournament.host_user,
                    name_in_tournament = host_name_in_tournament
                )

                for token_data in tournament_creation_serializer_validated_data['tokens']:
                    if token_data.custom_name is not None:
                        guest_name_in_tournament = token_data.custom_name
                    else:
                        guest_name_in_tournament = token_data.guest_user.username
                        
                    TournamentParticipant.objects.create(
                        tournament = tournament,
                        user = token_data.guest_user,
                        name_in_tournament = guest_name_in_tournament
                    )
                
                TournamentSetupManager.setup_matchups(tournament.id)

                return tournament.id
                
        except Exception as e:
            raise TournamentCreationException(f"An error occurred while creating tournament and its participants: {e}")

    @staticmethod
    def setup_matchups(tournament_id):
        try:
            tournament = Tournament.objects.get(pk=tournament_id)
        except Tournament.DoesNotExist:
            raise TournamentInProgressException("Tournament does not exist.")
        
        if tournament.state != TournamentState.IN_PROGRESS or tournament.next_match != 0:
            raise TournamentInProgressException("Tournament is not in a valid state to set up matchups.")
        
        participants = list(tournament.participants.all())
        if len(participants) != tournament.player_amount:
            raise TournamentInProgressException("The number of participants does not match the expected player amount.")
        
        total_matchups = tournament.player_amount - 1

        try:
            with transaction.atomic():

                # SETUP OF INITIAL MATCHUPS ARE DONE BASED ON THE ORDER OF PARTICIPANTS
                # IF YOU WANT TO TO SET UP INITIAL MATCHUPS BASED ON SOME OTHER ALGORITHM, PUT IT HERE
                for i in range(0, len(participants), 2):
                    TournamentMatchup.objects.create(
                        tournament=tournament,
                        player1=participants[i],
                        player2=participants[i + 1],
                        tournament_match_id=i // 2
                    )

                # CREATE EMPTY MATCHUPS FOR THE SUBSEQUENT MATCHES IN THE TOURNAMENT
                # THE MATCH WINNERS WILL BE ASSIGNED TO THEM LATER ON
                for matchup_id in range(len(participants) // 2, total_matchups):
                    TournamentMatchup.objects.create(
                        tournament=tournament,
                        tournament_match_id=matchup_id
                    )
                    
                tournament.start_ts = datetime.now()
                tournament.save()

        except Exception as e:
            raise TournamentInProgressException(f"An error occurred while setting up matchups: {e}")


class TournamentInProgressManager:
    @staticmethod
    def make_sure_users_in_ongoing_tournament_are_still_active(tournament) -> None:
        if not isinstance(tournament, Tournament):
            raise TypeError((f'function input must be a Tournament, not {type(tournament).__name__}'))
        
        participants = TournamentParticipant.objects.filter(tournament=tournament)
        inactive_users = participants.filter(user__is_active=False)
        if inactive_users.exists():
            tournament.abort_tournament()
            raise TournamentInProgressException(f"An user in ongoing tournament has deleted their account; tournament aborted")

        return True
    
from django.db import transaction

class TournamentInProgressManager:
    @staticmethod
    def assign_winning_participant_to_next_matchup_with_empty_participant_slot(winning_participant: TournamentParticipant) -> None:
        try:
            with transaction.atomic():
                tournament = winning_participant.tournament
                try:
                    coming_matchups = TournamentMatchup.objects.filter(
                        tournament=tournament,
                        tournament_match_id__gte=tournament.next_match
                    ).order_by('tournament_match_id')

                except TournamentMatchup.DoesNotExist:
                    raise TournamentInProgressException("No future matchup with empty participant slot")
                
                for matchup in coming_matchups:
                    if matchup.participant_left_side is None:
                        matchup.participant_left_side = winning_participant
                        matchup.save()
                        return
                    elif matchup.participant_right_side is None:
                        matchup.participant_right_side = winning_participant
                        matchup.save()
                        return
                    
                raise TournamentInProgressException("No future matchup with empty participant slot")

        except Exception as e:
            raise TournamentInProgressException(f"An error occurred while assigning the winning participant to future matchup: {e}")
        
    @staticmethod
    def update_tournament_with_winning_participant(winning_participant: TournamentParticipant) -> None:
        try:
            with transaction.atomic():
                tournament = winning_participant.tournament
                next_matchup_id = tournament.next_match
                
                try:
                    next_matchup = TournamentMatchup.objects.get(
                        tournament=tournament,
                        tournament_match_id=next_matchup_id
                    )
                except TournamentMatchup.DoesNotExist:
                    tournament.winner = winning_participant.user
                    tournament.state = TournamentState.FINISHED
                    tournament.save()
                    return
                
                TournamentInProgressManager.assign_winning_participant_to_next_matchup_with_empty_participant_slot(winning_participant)

        except Exception as e:
            raise TournamentInProgressException(f"An error occurred while updating tournament data after finished match: {e}")



        
