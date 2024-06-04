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
	def create_tournament_and_its_players(tournament_creation_serializer):
		try:
			with transaction.atomic:
				
				Tournament.objects.create(
					host_user = 
				)

