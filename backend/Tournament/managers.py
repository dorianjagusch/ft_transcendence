from django.db import models, transaction, IntegrityError
from django.core.exceptions import ValidationError
from datetime import datetime
from .models import Tournament, \
      					TournamentParticipant, \
                        TournamentMatchup, \
                        TournamentState
from .exceptions import TournamentCreationException, \
      						TournamentInProgressException
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
					guest_token = TournamentGuestToken.objects.get(token=token_data)
					if guest_token.custom_name is not None:
						guest_name_in_tournament = guest_token.custom_name
					else:
						guest_name_in_tournament = guest_token.guest_user.username
						
					TournamentParticipant.objects.create(
						tournament = tournament,
						user = guest_token.guest_user,
						name_in_tournament = guest_name_in_tournament
					)

				return tournament
				
		except Exception as e:
			raise TournamentCreationException(f"An error occurred while creating tournament and its participants: {e}")


class TournamentInProgressManager:
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
        
        # Calculate the total number of matchups
        total_matchups = tournament.player_amount - 1

        try:
            with transaction.atomic():
                # Setup initial matchups with participants
                for i in range(0, len(participants), 2):
                    TournamentMatchup.objects.create(
                        tournament=tournament,
                        player1=participants[i],
                        player2=participants[i + 1],
                        tournament_match_id=i // 2
                    )
                
                # Create empty matchups for the subsequent rounds
                for matchup_id in range(len(participants) // 2, total_matchups):
                    TournamentMatchup.objects.create(
                        tournament=tournament,
                        tournament_match_id=matchup_id
                    )
                    
                tournament.start_ts = datetime.now()
                tournament.save()
        except Exception as e:
            raise TournamentInProgressException(f"An error occurred while setting up matchups: {e}")

