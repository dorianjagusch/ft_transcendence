from django.db import models, transaction, IntegrityError

from .models import Match
from Tokens.models import MatchToken
from User.models import User
from Player.models import Player

import sys

class MatchSetupManager:
	@staticmethod
	def create_match_and_its_players(match_token):
		if not isinstance(match_token, MatchToken):
			raise TypeError((f'match_token must be an MatchToken, not {type(match_token).__name__}'))
		
		try:
			with transaction.atomic():
				# modify later to take into consideration tournament data
				match = Match.objects.create()
				
				player_left_side = Player.objects.create(
					user_id=match_token.user_left_side.id,
					match=match,
					score=0,
					match_winner=False
				)
				
				player_right_side = Player.objects.create(
					user_id=match_token.user_right_side.id,
					match=match,
					score=0,
					match_winner=False
				)
		
		except IntegrityError as e:
			print(f"integrity error: An error occurred: {e}", file=sys.stderr)
			return None, None, None
		except Exception as e:
			print(f"An error occurred: {e}", file=sys.stderr)
			return None, None, None
		
		return match, player_left_side, player_right_side