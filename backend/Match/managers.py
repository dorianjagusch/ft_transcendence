from django.db import models, transaction, IntegrityError
from django.db.models import Q

from .PlayerMatchStatus import PlayerMatchStatus
from Player.models import Player
from User.models import User

import sys

class MatchManager(models.Manager):
	def create_match_and_its_players(self, left_side_user_id, right_side_user_id):
		try:
			with transaction.atomic():
				match = self.create()
				
				player_left_side = Player.objects.create(
					user_id=left_side_user_id,
					match=match,
					score=0,
					match_winner=False
				)
				
				player_right_side = Player.objects.create(
					user_id=right_side_user_id,
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


	def get_match_players(self, match_id):
		try:
			players = Player.objects.filter(match_id=match_id)
		except Player.DoesNotExist:
			raise ValueError("No players found for Match with id '{}'.".format(match_id))
		
		return players

	def get_match_by_player_id(self, player_id):
		try:
			player = Player.objects.select_related('match').get(id=player_id)
		except Player.DoesNotExist:
			raise ValueError("Player with id '{}' does not exist.".format(player_id))

		return player.match

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
