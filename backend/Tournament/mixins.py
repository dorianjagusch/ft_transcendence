from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from .models import Tournament
from .serializers import TournamentSerializers
from .managers import TournamentManager
from .exceptions import TournamentInProgressException
from .tournamentState import TournamentState
from User.models import User
from User.mixins import AuthenticateUserMixin
from Tokens.mixins import CreateTournamentMatchTokenMixin


class CreateTournamentMixin:
	"""
	Mixin for creating a tournament.
	Will create a tournament and a tournament player for the host.
	"""
	def create_tournament(self, request: Request) -> Response:
		body_data = request.data.copy()
		body_data['host_user'] = request.user.id

		tournament_creation_serializer = TournamentSerializers.creation(data=body_data)
		if not tournament_creation_serializer.is_valid():
			return Response({"message": "Invalid request for tournament creation"}, status=status.HTTP_400_BAD_REQUEST)

		try:
			tournament = TournamentManager.create_tournament_and_tournament_player_for_host(tournament_creation_serializer.validated_data)
			if not tournament:
				return Response({"message" : "Tournament was not found"}, status=status.HTTP_404_NOT_FOUND)
			host_tournament_player_serializer = TournamentSerializers.player(tournament.players.all().first())
			return Response({
				'tournament': TournamentSerializers.default(tournament).data,
				'tournament_player': host_tournament_player_serializer.data
			}, status=status.HTTP_201_CREATED)
		except Exception as e:
			return Response({"message": "Creating a tournament failed"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TournamentDetailMixin:
	"""
	Mixin for getting tournament details.
	The response will have a different tournament serializer depending
	on if the user is the host of the ongoing tournament or not.
	"""
	def get_tournament_details(self, request: Request, tournament_id: int) -> Response:
		tournament = Tournament.objects.filter(id=tournament_id).first()
		if not tournament:
			return Response({"message" : f"Tournament {tournament_id} not found."}, status=status.HTTP_404_NOT_FOUND)
		if request.user == tournament.host_user and tournament.state == TournamentState.IN_PROGRESS:
			serializer = TournamentSerializers.in_progress(tournament)
		else:
			serializer = TournamentSerializers.default(tournament)
		return Response(serializer.data, status=status.HTTP_200_OK)

class ChangeTournamentStateMixin:
	"""
	Mixin for changing a tournament's state.
	If tournament's state is LOBBY, start tournament.
	If tournament's state is IN_PROGRESS, abort tournament.
	"""
	def change_tournament_state(self, tournament_id: int) -> Response:
		tournament = Tournament.objects.get(id=tournament_id)
		if tournament.state == TournamentState.LOBBY:
			try:
				TournamentManager.start_tournament(tournament)
				serializer = TournamentSerializers.in_progress(tournament)
				return Response(serializer.data, status=status.HTTP_200_OK)
			except Exception as e:
				return Response({"message": "Starting tournament failed."}, status=status.HTTP_400_BAD_REQUEST)

		elif tournament.state == TournamentState.IN_PROGRESS:
			TournamentManager.abort_tournament(tournament)
			return Response({"message": "Tournament has been aborted."}, status=status.HTTP_200_OK)

class AbortTournamentMixin:
	"""
	Abort tournament whose state is LOBBY or IN_PROGRESS.
	"""
	def abort_tournament(self, tournament_id: int) -> Response:
		tournament = Tournament.objects.filter(id=tournament_id).first()
		TournamentManager.abort_tournament(tournament)
		return Response({"message": "Tournament has been aborted."}, status=status.HTTP_200_OK)

class GetTournamentPlayersMixin:
	"""
	Mixin for getting a specific tournament's players.
	"""
	def get_tournament_players(self, tournament_id: int) -> Response:
		tournament = Tournament.objects.filter(id=tournament_id).first()
		if not tournament:
			return Response({"message" : f"Tournament {tournament_id} not found."}, status=status.HTTP_404_NOT_FOUND)
		tournament_players = tournament.players.all().order_by('id')
		tournament_players_serializers = TournamentSerializers.player(tournament_players, many=True)
		return Response(tournament_players_serializers.data, status=status.HTTP_200_OK)
	
class CreateTournamentPlayerMixin(AuthenticateUserMixin):
	"""
	Mixin for creating a player for a tournament.
	"""
	def create_tournament_player(self, request: Request, tournament_id: int) -> Response:
		result = self.authenticate_user(request)
		if not isinstance(result, User):
			response = result
			return response
		
		tournament = Tournament.objects.get(id=tournament_id)
		if tournament.players.count() >= tournament.player_amount:
			return Response({"message": "Tournament already has maximum number of players"}, status=status.HTTP_400_BAD_REQUEST)

		user = result
		username = user.username
		display_name = request.data.get('display_name', None)
		try:
			tournament_player = TournamentManager.create_tournament_player(tournament, user, display_name or username)
			tournament_player_serializer = TournamentSerializers.player(tournament_player)
			return Response(tournament_player_serializer.data, status=status.HTTP_201_CREATED)
		except Exception as e:
			return Response({"message": "Creating a tournament player failed"}, status=status.HTTP_400_BAD_REQUEST)

class TournamentPlayerDetailMixin:
	"""
	Mixin for getting tournament player details.
	"""
	def get_tournament_player_details(self, tournament_id: int, tournamentplayer_id: int) -> Response:
		tournament = Tournament.objects.filter(id=tournament_id).first()
		tournament_player = tournament.players.filter(id=tournamentplayer_id).first()
		if not tournament_player:
			return Response({"message": f"Tournament {tournament.id} does not have tournamentplayer with id {tournamentplayer_id}"}, status=status.HTTP_404_NOT_FOUND)

		tournament_player_serializer = TournamentSerializers.player(tournament_player)
		return Response(tournament_player_serializer.data, status=status.HTTP_200_OK)

class DeleteTournamentPlayerMixin:
	"""
	Mixin for deleting a tournament player from tournament in LOBBY state.
	"""
	def delete_tournament_player(self, request: Request, tournament_id: int, tournamentplayer_id: int) -> Response:
		tournament = Tournament.objects.get(id=tournament_id)
		tournament_player = tournament.players.filter(id=tournamentplayer_id).first()
		if not tournament_player:
			return Response({"message": f"Tournament {tournament.id} does not have tournamentplayer with id {tournamentplayer_id}"}, status=status.HTTP_404_NOT_FOUND)

		if tournament_player.user == request.user:
			return Response({"message": "Cannot delete host tournament player"}, status=status.HTTP_404_NOT_FOUND)
		tournament_player.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class GetTournamentMatchesMixin:
	"""
	Mixin for getting list of matches in a specific tournament.
	"""
	def get_tournament_matches(self, tournament_id: int) -> Response:
		tournament = Tournament.objects.filter(id=tournament_id).first()
		if not tournament:
			return Response({"message" : f"Tournament {tournament_id} not found."}, status=status.HTTP_404_NOT_FOUND)
		tournament_matches = tournament.matches.all().order_by('id')
		tournament_match_serializers = TournamentSerializers.match(tournament_matches, many=True)
		return Response(tournament_match_serializers.data, status=status.HTTP_200_OK)

class TournamentMatchDetailMixin(CreateTournamentMatchTokenMixin):
	"""
	Mixin for getting details of a specific match in a tournament.
	If the requester is the host of the tournament in IN_PROGRESS state
	and the match is the next match to be played in the tournament, returns the match game url.
	"""
	def get_tournament_match_details(self, request: Request, tournament_id: int, tournament_match_id: int) -> Response:
		tournament = Tournament.objects.get(id=tournament_id)
		if not tournament:
			return Response({"message" : f"Tournament {tournament_id} not found"}, status=status.HTTP_404_NOT_FOUND)
		tournament_matches = tournament.matches.all().order_by('id')
		if tournament_match_id >= tournament_matches.count():
			return Response({"message": f"Tournament {tournament_id} does not have {tournament_match_id} match"}, status=status.HTTP_404_NOT_FOUND)

		if request.user == tournament.host_user \
			and tournament.state == TournamentState.IN_PROGRESS \
			and tournament_matches.filter(state=TournamentState.FINISHED).count() == tournament_match_id:

			try:
				TournamentManager.raise_error_if_tournament_has_expired(tournament)
				TournamentManager.raise_error_if_inactive_user_in_tournament(tournament)
			except TournamentInProgressException as e:
				TournamentManager.abort_tournament(tournament)
				return Response({"message" : f"{str(e)}; tournament aborted!"}, status=status.HTTP_400_BAD_REQUEST)

			if tournament_matches[tournament_match_id].state != TournamentState.LOBBY:
				return Response({"message": f"The tournament match {tournament_match_id} is not in LOBBY state"}, status=status.HTTP_400_BAD_REQUEST)
			next_match = tournament_matches[tournament_match_id]
			token = self.create_tournament_match_token(next_match)
			pong_match_url = f'wss://localhost:8443/pong/{next_match.id}?token={token.token}'
			return Response(pong_match_url, status=status.HTTP_200_OK)

		else:
			tournament_match_serializer = TournamentSerializers.match(tournament_matches[tournament_match_id])
			return Response(tournament_match_serializer.data, status=status.HTTP_200_OK)

class ChangeDeletedUserTournamentNamesMixin:
	"""
    Mixin that changes a user's tournamentplayers' display names to deleted_user.
	Use only when deleting a user.
    """
	def change_tournament_player_names_to_deleted(self, user: User) -> None:
		tournament_players = user.tournament_players.all()
		for player in tournament_players:
			player.display_name = "deleted_user"
			player.save()
