from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator

from .models import Tournament, \
						TournamentState
from .serializers import TournamentOutputSerializer, \
							TournamentCreationSerializer, \
							TournamentInProgressSerializer
from .managers import TournamentSetupManager, \
						TournamentInProgressManager
from .exceptions import TournamentCreationException, \
							TournamentInProgressException
from Tokens.models import MatchToken
from Match.models import Match

from shared_utilities.decorators import must_be_authenticated

import sys

class TournamentListView(APIView):
	@method_decorator(must_be_authenticated)
	def post(self, request):
		serializer = TournamentCreationSerializer(data=request.data, context={'request': request})
		if serializer.is_valid():
			validated_data = serializer.validated_data
			try:
				tournament_id = TournamentSetupManager.create_tournament_and_its_tournament_players(validated_data)
				tournament_url = f"http://localhost:8080/tournaments/{tournament_id}"
				return Response(tournament_url, status=status.HTTP_201_CREATED)
			except TournamentCreationException as e:
				return Response({'error': str(e)}, status=e.status_code)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TournamentDetailView(APIView):
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

