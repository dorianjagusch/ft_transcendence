from django.db import models, transaction, IntegrityError
from django.db.models import Q

from .playerMatchStatus import PlayerMatchStatus
from .exceptions import MatchAndPlayersCreationException
from Player.models import Player
from User.models import User

import sys

class MatchManager(models.Manager):
	def get_matches_with_user(self, user_id, match_status):
		try:
			user = User.objects.get(pk=user_id)
		except User.DoesNotExist:
			raise ValueError("User with id '{}' does not exist.".format(user_id))

		matches_with_user = self.filter(players__user_id=user_id)

		if match_status == PlayerMatchStatus.WINS.value:
			matches_with_user = matches_with_user.filter(
				players__user_id=user_id, players__match_winner=True
			)
		elif match_status == PlayerMatchStatus.LOSSES.value:
			matches_with_user = matches_with_user.filter(
				players__user_id=user_id, players__match_winner=False
			)

		return matches_with_user

class MatchSetupManager:
	@staticmethod
	def create_match_and_its_players(match_token):
		from Tokens.models import MatchToken
		from .models import Match

		if not isinstance(match_token, MatchToken):
			raise TypeError((f'match_token must be an MatchToken, not {type(match_token).__name__}'))
		
		try:
			with transaction.atomic():
				match = Match.objects.create(
					tournament_matchup=match_token.tournament_matchup
				)
				
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
			raise MatchAndPlayersCreationException(f"An error occurred while creating match and/or players: {e}")
		
		return match