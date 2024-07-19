from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator

from .models import Tournament, \
						TournamentPlayer
from .serializers import TournamentSerializers
from .managers import TournamentManager
from .exceptions import TournamentSetupException, \
							TournamentInProgressException
from .tournamentState import TournamentState
from User.models import User
from Tokens.models import MatchToken
from Tokens.managers import MatchTokenManager
from Match.matchState import MatchState
from shared_utilities.decorators import must_be_authenticated, \
											must_not_be_username, \
											validate_tournament_request

import sys

# Create your views here.
class TournamentListView(APIView):
	@method_decorator(must_be_authenticated)
	def post(self, request):
		body_data = request.data.copy()
		body_data['host_user'] = request.user.id

		tournament_creation_serializer = TournamentSerializers.creation(data=body_data)
		if not tournament_creation_serializer.is_valid():
			return Response({'error': 'invalid request for tournament creation'}, status=status.HTTP_400_BAD_REQUEST)
		
		try:
			tournament = TournamentManager.setup.create_tournament_and_tournament_player_for_host(tournament_creation_serializer.validated_data)
			host_tournament_player_serializer = TournamentSerializers.player(tournament.players.all().first())
			return Response({
				'tournament_id': tournament.id,
				'tournament_player': host_tournament_player_serializer.data
			}, status=status.HTTP_201_CREATED) 
		except Exception as e:
			return Response({'error': str(e)},status=status.HTTP_403_FORBIDDEN)
		
class TournamentDetailView(APIView):
	def get(self, request, tournament_id):
		tournament = Tournament.objects.filter(id=tournament_id).first()
		if not tournament:
			return Response(f"Tournament {tournament_id} not found.", status=status.HTTP_404_NOT_FOUND)
		if request.user == tournament.host_user and tournament.state == TournamentState.IN_PROGRESS:
			serializer = TournamentSerializers.in_progress(tournament)
		else:
			serializer = TournamentSerializers.default(tournament)
		return Response(serializer.data, status=status.HTTP_200_OK)

	@method_decorator(must_be_authenticated)
	@method_decorator(validate_tournament_request([TournamentState.LOBBY]))
	def post(self, request, tournament_id):
		'''starts the tournament.
		'''
		tournament = Tournament.objects.get(id=tournament_id)
		try:
			TournamentManager.setup.start_tournament(tournament)
			serializer = TournamentSerializers.in_progress(tournament)
			return Response(serializer.data, status=status.HTTP_200_OK)
		except Exception as e:
			return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)

	@method_decorator(must_be_authenticated)
	@method_decorator(validate_tournament_request([TournamentState.LOBBY, TournamentState.IN_PROGRESS]))
	def delete(self, request, tournament_id):
		tournament = Tournament.objects.filter(id=tournament_id).first()
		TournamentManager.in_progress.abort_tournament(tournament)
		return Response({"message": "Tournament has been abandoned."}, status=status.HTTP_200_OK)

class TournamentPlayerListView(APIView):
	def get(self, request, tournament_id):
		tournament = Tournament.objects.filter(id=tournament_id).first()
		if not tournament:
			return Response(f"Tournament {tournament_id} not found.", status=status.HTTP_404_NOT_FOUND)
		tournament_players = tournament.players.all().order_by('id')
		tournament_players_serializers = TournamentSerializers.player(tournament_players, many=True)
		return Response(tournament_players_serializers.data, status=status.HTTP_200_OK)

	@method_decorator(must_be_authenticated)
	@method_decorator(validate_tournament_request([TournamentState.LOBBY]))
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
			return Response({"error": "Tournament already has maximum number of players"}, status=status.HTTP_400_BAD_REQUEST)

		try:
			tournament_player = TournamentManager.players.create_tournament_player(tournament, user, display_name)
			tournament_player_serializer = TournamentSerializers.player(tournament_player)
			return Response(tournament_player_serializer.data, status=status.HTTP_201_CREATED)
		except Exception as e:
			return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)

class TournamentPlayerDetailView(APIView):
	def get(self, request, tournament_id, tournamentplayer_id):
		tournament = Tournament.objects.filter(id=tournament_id).first()
		tournament_player = tournament.players.filter(id=tournamentplayer_id).first()
		if not tournament_player:
			return Response({'error': f'Tournament {tournament.id} does not have tournamentplayer with id {tournamentplayer_id}'}, status=status.HTTP_404_NOT_FOUND)
		
		tournament_player_serializer = TournamentSerializers.player(tournament_player)
		return Response(tournament_player_serializer.data, status=status.HTTP_200_OK)

	@method_decorator(must_be_authenticated)
	@method_decorator(validate_tournament_request([TournamentState.LOBBY]))
	def delete(self, request, tournament_id, tournamentplayer_id):
		tournament = Tournament.objects.get(id=tournament_id)
		tournament_player = tournament.players.filter(id=tournamentplayer_id).first()
		if not tournament_player:
			return Response({'error': f'Tournament {tournament.id} does not have tournamentplayer with id {tournamentplayer_id}'}, status=status.HTTP_404_NOT_FOUND)
		
		if tournament_player.user == request.user:
			return Response({'error': 'Cannot delete host tournament player'}, status=status.HTTP_404_NOT_FOUND)
		tournament_player.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class TournamentMatchListView(APIView):
	def get(self, request, tournament_id):
		tournament = Tournament.objects.filter(id=tournament_id).first()
		if not tournament:
			return Response(f"Tournament {tournament_id} not found.", status=status.HTTP_404_NOT_FOUND)
		tournament_matches = tournament.matches.all().order_by('id')
		tournament_match_serializers = TournamentSerializers.match(tournament_matches, many=True)
		return Response(tournament_match_serializers.data, status=status.HTTP_200_OK)

class TournamentMatchDetailView(APIView):
	# @method_decorator(must_be_authenticated)
	# @method_decorator(validate_tournament_request([TournamentState.IN_PROGRESS]))
	def get(self, request, tournament_id, tournament_match_id):
		'''get details of a single tournament match.
		If host and tournament is in progress and the tournament_match_id is the next_match, return match url.
		'''
		tournament = Tournament.objects.get(id=tournament_id)
		if not tournament:
			return Response(f"Tournament {tournament_id} not found", status=status.HTTP_404_NOT_FOUND)
		tournament_matches = tournament.matches.all().order_by('id')
		if tournament_match_id >= tournament_matches.count():
			return Response(f"Tournament {tournament_id} does not have {tournament_match_id} match", status=status.HTTP_404_NOT_FOUND)
		# check if user is host, tournament is in progress, and the tournament_match_id is the next_match, if so, start match
		if request.user == tournament.host_user \
			and tournament.state == TournamentState.IN_PROGRESS \
			and tournament_matches.filter(state=TournamentState.FINISHED).count() == tournament_match_id:
			if tournament_matches[tournament_match_id].state != TournamentState.LOBBY:
				return Response({"error": f"the tournament match {tournament_match_id} is not in LOBBY state"}, status=status.HTTP_400_BAD_REQUEST)
			next_match = tournament_matches[tournament_match_id]
			token = MatchTokenManager.create_tournament_match_token(next_match)
			pong_match_url = f'ws://localhost:8080/pong/{next_match.id}?token={token.token}'
			return Response(pong_match_url, status=status.HTTP_200_OK)
		else:
			tournament_match_serializer = TournamentSerializers.match(tournament_matches[tournament_match_id])
			return Response(tournament_match_serializer.data, status=status.HTTP_200_OK)

