from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator

from .models import Tournament, \
						TournamentPlayer, \
						TournamentState
from .serializers import TournamentOutputSerializer, \
							TournamentCreationSerializer, \
							TournamentInProgressSerializer, \
							TournamentPlayerSerializer
from .managers import TournamentSetupManager, \
						TournamentInProgressManager
from .exceptions import TournamentCreationException, \
							TournamentInProgressException
from Tokens.models import MatchToken, TournamentToken
from Tokens.serializers import TournamentTokenSerializer
from Match.models import Match

from shared_utilities.decorators import must_be_authenticated, \
											check_that_valid_tournament_token

import sys

class TournamentListView(APIView):
	@method_decorator(must_be_authenticated)
	def post(self, request):
		data_to_serialize = request.data.copy()
		data_to_serialize['host_user'] = request.user
		serializer = TournamentCreationSerializer(data=data_to_serialize)
		if serializer.is_valid():
			try:
				tournament = TournamentSetupManager.create_tournament_and_host_tournament_player(serializer.validated_data)
				tournament_token = TournamentToken.objects.create_tournament_token(tournament)
				serializer = TournamentTokenSerializer(tournament_token)
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			except TournamentCreationException as e:
				return Response({'error': str(e)}, status=e.status_code)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TournamentPlayerListView(APIView):
	@method_decorator(must_be_authenticated)
	@method_decorator(check_that_valid_tournament_token)
	def post(self, request):
		'''Authenticate guest user and add them to tournament as tournament player.

		Body has to have 'token', 'username', and 'password'.
		Optionally can also have 'display_name'.
		Token must be active.
		'''
		tournament = TournamentToken.objects.get(token=request.data.get('token')).tournament
		if tournament.players.count() >= tournament.player_amount:
			return Response({'error': 'tournament is already full'}, status=status.HTTP_403_FORBIDDEN)
		username = request.data.get('username', None)
		password = request.data.get('password', None)
		display_name = request.data.get('display_name', None)
		if not tournament or not username or not password:
			return Response({'error': 'missing token, username, or password'}, status=status.HTTP_400_BAD_REQUEST)
		
		user = authenticate(request, username=username, password=password)
		if user is not None:
			tournament_player = TournamentSetupManager.add_user_to_tournament_as_tournament_player(tournament, user, display_name)
			serializer = TournamentPlayerSerializer(tournament_player)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response({"message": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)
		
class TournamentPlayerDetailView(APIView):
	def get(self, request, tournamentplayer_id):
		try:
			tournament_player = TournamentPlayer.objects.get(id=tournamentplayer_id)
			serializer = TournamentPlayerSerializer(tournament_player)
			return Response(serializer.data, status=status.HTTP_200_OK)
		except TournamentPlayer.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
	@method_decorator(must_be_authenticated)
	def delete(self, request, tournamentplayer_id):
		try:
			tournament_player = TournamentPlayer.objects.get(id=tournamentplayer_id)
		except TournamentPlayer.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		if tournament_player.tournament.state != TournamentState.LOBBY:
			return Response({"error": "Cannot delete tournament player because tournament is not in lobby"}, status=status.HTTP_403_FORBIDDEN)
		if request.user != tournament_player.tournament.host_user:
			return Response({"error": "You are not the host of the tournament"}, status=status.HTTP_401_UNAUTHORIZED)
		
		tournament_player.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
		


class OLD_TournamentListView(APIView):
	@method_decorator(must_be_authenticated)
	def post(self, request):
		serializer = TournamentCreationSerializer(data=request.data, context={'request': request})
		if serializer.is_valid():
			validated_data = serializer.validated_data
			try:
				tournament_id = TournamentSetupManager.create_tournament_and_its_participants(validated_data)
				tournament_url = f"http://localhost:8080/tournaments/{tournament_id}"
				return Response(tournament_url, status=status.HTTP_201_CREATED)
			except TournamentCreationException as e:
				return Response({'error': str(e)}, status=e.status_code)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OLD_TournamentDetailView(APIView):
	def get(self, request, tournament_id):
		login_user_id = request.user.id
		try:
			tournament = Tournament.objects.get(pk=tournament_id)
		except Tournament.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		if login_user_id == tournament.host_user.id and tournament.state == TournamentState.IN_PROGRESS:
			try:
				TournamentInProgressManager.make_sure_active_tournament_is_still_valid(tournament)
			except TournamentInProgressException as e:
				TournamentInProgressManager.abort_tournament(tournament)
				return Response({'error': f'{e}'}, status=status.HTTP_403_FORBIDDEN)

			serializer = TournamentInProgressSerializer(tournament)
			return Response(serializer.data) 

		serializer = TournamentOutputSerializer(tournament)
		return Response(serializer.data)

	@method_decorator(must_be_authenticated)
	def post(self, request, tournament_id):
		login_user_id = request.user.id
		try:
			tournament = Tournament.objects.get(pk=tournament_id)
		except Tournament.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		if login_user_id != tournament.host_user.id:
			return Response({'error': 'You are not the tournament host'}, status=status.HTTP_403_FORBIDDEN)
		if tournament.state != TournamentState.IN_PROGRESS:
			return Response({'error': 'Tournament is not in progress'}, status=status.HTTP_403_FORBIDDEN)
		
		try:
			TournamentInProgressManager.make_sure_active_tournament_is_still_valid(tournament)
		except TournamentInProgressException as e:
			TournamentInProgressManager.abort_tournament(tournament)
			return Response({'error': f'{e}'}, status=status.HTTP_403_FORBIDDEN)
		
		try:
			token = MatchToken.objects.create_tournament_match_token_for_next_match(tournament)
		except Exception as e:
			return Response({'error': f'{e}]'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		
		match_id = Match.objects.get(tournament_match_id=tournament.next_match).pk
		pong_match_url = f'ws://localhost:8080/pong/{match_id}?token={token.token}'
		return Response(pong_match_url, status=status.HTTP_200_OK)

	@method_decorator(must_be_authenticated)
	def delete(self, request, tournament_id):
		login_user_id = request.user.id
		try:
			tournament = Tournament.objects.get(pk=tournament_id)
		except Tournament.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		if login_user_id != tournament.host_user.id:
			return Response({'error': 'You are not the tournament host'}, status=status.HTTP_403_FORBIDDEN)
		if tournament.state != TournamentState.IN_PROGRESS:
			return Response({'error': 'Tournament is not in progress'}, status=status.HTTP_403_FORBIDDEN)
		
		TournamentInProgressManager.abort_tournament(tournament)
		serializer = TournamentOutputSerializer(tournament)
		return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

