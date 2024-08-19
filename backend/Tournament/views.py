from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from django.utils.decorators import method_decorator

from .tournamentState import TournamentState
from .mixins import (
	CreateTournamentMixin, TournamentDetailMixin, ChangeTournamentStateMixin,
	AbortTournamentMixin, GetTournamentPlayersMixin, CreateTournamentPlayerMixin,
	TournamentPlayerDetailMixin, DeleteTournamentPlayerMixin, GetTournamentMatchesMixin,
	TournamentMatchDetailMixin
)
from shared_utilities.decorators import must_be_authenticated, validate_tournament_request


class TournamentListView(APIView, CreateTournamentMixin):
	@method_decorator(must_be_authenticated)
	def post(self, request: Request) -> Response:
		return self.create_tournament(request)

class TournamentDetailView(APIView, TournamentDetailMixin, ChangeTournamentStateMixin, AbortTournamentMixin):
	@method_decorator(must_be_authenticated)
	def get(self, request: Request, tournament_id: int) -> Response:
		return self.get_tournament_details(request, tournament_id)

	@method_decorator(must_be_authenticated)
	@method_decorator(validate_tournament_request([TournamentState.LOBBY, TournamentState.IN_PROGRESS]))
	def patch(self, request: Request, tournament_id: int) -> Response:
		return self.change_tournament_state(tournament_id)

	@method_decorator(must_be_authenticated)
	@method_decorator(validate_tournament_request([TournamentState.LOBBY, TournamentState.IN_PROGRESS]))
	def delete(self, request: Request, tournament_id: int) -> Response:
		return self.abort_tournament(tournament_id)

class TournamentPlayerListView(APIView, GetTournamentPlayersMixin, CreateTournamentPlayerMixin):
	@method_decorator(must_be_authenticated)
	def get(self, request: Request, tournament_id: int) -> Response:
		return self.get_tournament_players(tournament_id)

	@method_decorator(must_be_authenticated)
	@method_decorator(validate_tournament_request([TournamentState.LOBBY]))
	def post(self, request: Request, tournament_id: int) -> Response:
		return self.create_tournament_player(request, tournament_id)

class TournamentPlayerDetailView(APIView, TournamentPlayerDetailMixin, DeleteTournamentPlayerMixin):
	@method_decorator(must_be_authenticated)
	def get(self, request, tournament_id, tournamentplayer_id):
		self.get_tournament_player_details(tournament_id, tournamentplayer_id)

	@method_decorator(must_be_authenticated)
	@method_decorator(validate_tournament_request([TournamentState.LOBBY]))
	def delete(self, request, tournament_id, tournamentplayer_id):
		return self.delete_tournament_player(request, tournament_id, tournamentplayer_id)

class TournamentMatchListView(APIView, GetTournamentMatchesMixin):
	@method_decorator(must_be_authenticated)
	def get(self, request: Request, tournament_id: int) -> Response:
		return self.get_tournament_matches(tournament_id)

class TournamentMatchDetailView(APIView, TournamentMatchDetailMixin):
	@method_decorator(must_be_authenticated)
	def get(self, request, tournament_id, tournament_match_id):
		return self.get_tournament_match_details(request, tournament_id, tournament_match_id)

