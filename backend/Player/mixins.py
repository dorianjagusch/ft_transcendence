from rest_framework.response import Response
from rest_framework import status
from django.db.models.query import QuerySet

from .models import Player
from Match.models import Match

class GetAllPlayersMixin:
	'''
	Mixin to get all match players.
	'''
	def get_all_players(self) -> QuerySet:
		return Player.objects.all().order_by('id')
	
class GetPlayerMixin:
	'''
	Get a specific match player.
	'''
	def get_player(self, player_id: int) -> Player | Response:
		player = Player.objects.filter(pk=player_id).first()
		if not player:
			return Response({"message": "Player not found."}, status=status.HTTP_404_NOT_FOUND)
		
		return player

class GetMatchPlayersMixin:
	'''
	Get players of a specific match.
	'''
	def get_match_players(self, match_id: int) -> QuerySet | Response:
		match = Match.objects.filter(pk=match_id).first()
		if not match:
			return Response({"message": "Match not found."}, status=status.HTTP_404_NOT_FOUND)
		
		return match.players.all().order_by('id')