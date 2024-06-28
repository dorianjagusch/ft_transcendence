from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator

from .models import Tournament, \
						TournamentPlayer
from .serializers import TournamentCreationSerializer, \
							TournamentPlayerSerializer
from .managers import TournamentSetupManager, \
						TournamentInProgressManager
from .exceptions import TournamentSetupException, \
							TournamentInProgressException
from .tournamentState import TournamentState
from User.models import User
from shared_utilities.decorators import must_be_authenticated, \
											must_not_be_username, \
											check_that_valid_tournament_lobby_request, \
											check_that_valid_tournament_in_progress_request, \
											check_that_tournament_players_are_still_active

# Create your views here.
class TournamentListView(APIView):
	@method_decorator(must_be_authenticated)
	def post(self, request):
		body_data = request.data.copy()
		body_data['host_user'] = request.user
		tournament_creation_serializer = TournamentCreationSerializer(body_data)
		if not tournament_creation_serializer.is_valid():
			return Response({'error': 'invalid request for tournament creation'}, status=status.HTTP_400_BAD_REQUEST)
		
		try:
			tournament = TournamentSetupManager.create_tournament_and_tournament_player_for_host(tournament_creation_serializer.validated_data)
			host_tournament_player_serializer = TournamentPlayerSerializer(tournament.players.all().first())
			return Response({
				'tournament_id': tournament.id,
				'tournament_player': host_tournament_player_serializer.data
			}, status=status.HTTP_201_CREATED) 
		except Exception as e:
			return Response(TournamentSetupException(e))

class TournamentPlayerListView(APIView):
	@method_decorator(must_be_authenticated)
	@method_decorator(check_that_valid_tournament_lobby_request)
	@method_decorator(must_not_be_username)
	def post(self, request, tournament_id):
		username = request.data.get('username', None)
		password = request.data.get('password', None)
		display_name = request.data.get('display_name', None)

		if not username or not password:
			return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)
		user = authenticate(username=username, password=password)
		if user is None:
			return Response({"message": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

		tournament = Tournament.objects.get(id=tournament_id)
		if tournament.players.count() >= tournament.player_amount:
			return Response({"error": "Tournament already has maximum number of players"}, status=status.HTTP_403_FORBIDDEN)

		try:
			tournament_player = TournamentPlayer.objects.create(
				tournament_id=tournament_id,
				user=user,
				display_name=display_name,
			)
			tournament_player_serializer = TournamentPlayerSerializer(tournament_player)
			return Response(tournament_player_serializer.data, status=status.HTTP_201_CREATED)
		except Exception as e:
			return Response(TournamentSetupException(e))

class TournamentPlayerDetailView(APIView):
	def get(self, request, tournament_id, tournamentplayer_id):
		tournament = Tournament.objects.get(id=tournament_id)
		tournament_player = tournament.players.filter(id=tournamentplayer_id).first()
		if not tournament_player.exists():
			return Response({'error': f'Tournament {tournament.id} does not have tournamentplayer with id {tournamentplayer_id}'}, status=status.HTTP_404_NOT_FOUND)
		
		tournament_player_serializer = TournamentPlayerSerializer(tournament_player)
		return Response(tournament_player_serializer.data, status=status.HTTP_200_OK)

	@method_decorator(must_be_authenticated)
	@method_decorator(check_that_valid_tournament_lobby_request)
	def delete(self, request, tournament_id, tournamentplayer_id):
		tournament = Tournament.objects.get(id=tournament_id)
		tournament_player = tournament.players.filter(id=tournamentplayer_id).first()
		if not tournament_player.exists():
			return Response({'error': f'Tournament {tournament.id} does not have tournamentplayer with id {tournamentplayer_id}'}, status=status.HTTP_404_NOT_FOUND)
		
		if tournament_player.user == request.user:
			return Response({'error': 'Cannot delete host tournament player'}, status=status.HTTP_404_NOT_FOUND)
		tournament_player.delete()
		tournament_player.save()
		return Response(status=status.HTTP_204_NO_CONTENT)