from django.db import models, transaction, IntegrityError

from .models import Tournament
from .serializers import FourPlayerTournamentCreationSerializer, \
							EightPlayerTournamentCreationSerializer
from Tokens.models import TournamentGuestToken
from User.models import User
from Player.models import Player

import sys


class TournamentSetupManager:
	@staticmethod
	def create_tournament_and_its_four_players(tournament_creation_serializer):
		if not isinstance(tournament_creation_serializer, FourPlayerTournamentCreationSerializer):
					 raise TypeError((f'tournament_creation_serializer must be an FourPlayerTournamentCreationSerializer, not {type(tournament_creation_serializer).__name__}'))
		 
		try:
			with transaction.atomic():

		except IntegrityError as e:
			print(f"integrity error: An error occurred: {e}", file=sys.stderr)
			return None, None, None
		except Exception as e:
			print(f"An error occurred: {e}", file=sys.stderr)
			return None, None, None
		  
	@staticmethod
	def create_tournament_and_its_eight_players(tournament_creation_serializer):
		if not isinstance(tournament_creation_serializer, FourPlayerTournamentCreationSerializer):
			raise TypeError((f'tournament_creation_serializer must be an EightPlayerTournamentCreationSerializer, not {type(tournament_creation_serializer).__name__}'))

	@staticmethod
	def create_tournament_and_its_eight_players(tournament_creation_serializer):

	@staticmethod
	def create_tournament_and_its_players(tournament_creation_serializer):
		if isinstance(tournament_creation_serializer, FourPlayerTournamentCreationSerializer) \
			and not isinstance(tournament_creation_serializer, EightPlayerTournamentCreationSerializer):
			# Logic for four-player tournament creation
			pass
		elif isinstance(tournament_creation_serializer, EightPlayerTournamentCreationSerializer):
			# Logic for eight-player tournament creation
			pass
		else:
			raise ValueError("Unsupported serializer type")

