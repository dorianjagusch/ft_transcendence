from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.utils.decorators import method_decorator

from .models import Player
from .serializers import PlayerSerializer
from .mixins import GetAllPlayersMixin, GetPlayerMixin, GetMatchPlayersMixin
from shared_utilities.decorators import must_be_authenticated

class PlayerListView(APIView, GetAllPlayersMixin):
	@method_decorator(must_be_authenticated)
	def get(self, request: Request) -> Response:
		all_players = self.get_all_players()
		serializer = PlayerSerializer(all_players, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)
	
class PlayerDetailView(APIView, GetPlayerMixin):
	@method_decorator(must_be_authenticated)
	def get(self, request: Request, player_id: int) -> Response:
		result = self.get_player(player_id)
		if not isinstance(result, Player):
			return result
		
		serializer = PlayerSerializer(result)
		return Response(serializer.data, status=status.HTTP_200_OK)
	
class MatchPlayerListView(APIView, GetMatchPlayersMixin):
	@method_decorator(must_be_authenticated)
	def get(self, request: Request, match_id: int) -> Response:
		result = self.get_match_players(match_id)
		if isinstance(result, Response):
			return result
		
		serializer = PlayerSerializer(result, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)