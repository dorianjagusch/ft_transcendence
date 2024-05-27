from django.db import models, transaction, IntegrityError
from django.db.models import Q

from .PlayerMatchStatus import PlayerMatchStatus
from Player.models import Player
from User.models import User

import sys

class MatchManager(models.Manager):
	def create_match_and_its_players(self, player_home_user_id, player_visiting_user_id):
		try:
			with transaction.atomic():
				match = self.create()
				
				player_home = Player.objects.create(
					user_id_id=player_home_user_id,
					match_id=match,
					score=0,
					match_winner=False
				)
				
				player_visiting = Player.objects.create(
					user_id_id=player_visiting_user_id,
					match_id=match,
					score=0,
					match_winner=False
				)
		
		except IntegrityError as e:
			print(f"integrity error: An error occurred: {e}", file=sys.stderr)
			return None, None, None
		except Exception as e:
			print(f"An error occurred: {e}", file=sys.stderr)
			return None, None, None
		
		return match, player_home, player_visiting


	def get_match_players(self, match_id):
		try:
			players = Player.objects.filter(pk=match_id)
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
