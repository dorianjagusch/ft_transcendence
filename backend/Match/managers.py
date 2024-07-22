from django.db import models, transaction, IntegrityError

from .models import Match
from Tokens.models import MatchToken
from User.models import User
from Player.models import Player

import sys

class MatchSetupManager:
	@staticmethod
	def create_match_and_its_players(match_token: MatchToken) -> Match | None:
		try:
			with transaction.atomic():
				match = Match.objects.create()
				
				Player.objects.create(
					user_id=match_token.user_left_side.id,
					match=match,
					score=0,
					match_winner=False
				)
				
				Player.objects.create(
					user_id=match_token.user_right_side.id,
					match=match,
					score=0,
					match_winner=False
				)

		except Exception as e:
			print(f"An error occurred: {e}", file=sys.stderr)
			return None
		
		return match