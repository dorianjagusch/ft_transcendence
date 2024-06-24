from django.db import models, transaction

from .playerMatchStatus import PlayerMatchStatus
from .exceptions import MatchAndPlayersCreationException, \
							MatchPlayersException
from .matchState import MatchState
from Player.models import Player
from User.models import User

import sys

class MatchManager(models.Manager):
	def get_matches_with_user(self, user_id, match_status):
		try:
			user = User.objects.get(pk=user_id)
		except User.DoesNotExist:
			raise ValueError(f"User with id '{user_id}' does not exist.")

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
	
	@staticmethod
	def abort_tournament_matches(self, tournament_id: int):
		tournament_matches = self.filter(
			tournament_id=tournament_id
		).order_by('tournament_match_id')

		for match in tournament_matches:
			if match.state in [MatchState.LOBBY, MatchState.IN_PROGRESS]:
				match.state = MatchState.ABORTED
				match.save()

class MatchSetupManager:
	@staticmethod
	def create_match_and_its_players(match_token):
		from Tokens.models import MatchToken
		from .models import Match

		if not isinstance(match_token, MatchToken):
			raise TypeError((f'function input must be MatchToken, not {type(match_token).__name__}'))
		
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

			return match.id
		
		except Exception as e:
			raise MatchAndPlayersCreationException(f"An error occurred while creating match and/or players: {e}")

	@staticmethod
	def make_sure_users_in_match_are_still_active(match):
		from Match.models import Match

		if not isinstance(match, Match):
			raise TypeError((f'function input must be Match, not {type(match).__name__}'))
		
		players = Match.players.filter(match=match)
		inactive_users = players.filter(user__is_active=False)
		if inactive_users.exists():
			match.abort_match()
			raise MatchPlayersException(f"An user in Match has deleted their account; match aborted")
