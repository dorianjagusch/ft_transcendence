from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator

from .models import Tournament, \
						TournamentMatchup, \
						TournamentState
from .serializers import TournamentOutputSerializer, \
							TournamentCreationSerializer, \
							TournamentInProgressSerializer
from .managers import TournamentSetupManager, \
						TournamentInProgressManager
from .exceptions import TournamentCreationException
from Tokens.managers import MatchTokenManager
from Match.managers import MatchSetupManager
from Match.exceptions import MatchAndPlayersCreationException

from shared_utilities.decorators import must_be_authenticated

@method_decorator(must_be_authenticated)
class StartTournamentView(APIView):
	def post(self, request):
		serializer = TournamentCreationSerializer(data=request.data, context={'request': request})
		if serializer.is_valid():
			validated_data = serializer.validated_data
			try:
				tournament = TournamentSetupManager.create_tournament_and_its_participants(validated_data)
				return Response({'tournament_id': tournament.id}, status=status.HTTP_201_CREATED)
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
			if tournament.current_match == 0:
				TournamentInProgressManager.setup_matchups(tournament_id)
			serializer = TournamentInProgressSerializer(tournament)
			return Response(serializer.data) 

		serializer = TournamentOutputSerializer(tournament)
		return Response(serializer.data)

class LaunchTournamentMatchView(APIView):
	def get(self, request, tournament_id, next_match):
		login_user_id = request.user.id
		try:
			tournament = Tournament.objects.get(pk=tournament_id)
		except Tournament.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		if login_user_id != tournament.host_user.id:
			return Response({'error': 'You are not the tournament host'}, status=status.HTTP_403_FORBIDDEN)
		if tournament.state != TournamentState.IN_PROGRESS:
			return Response({'error': 'Tournament is not in progress'}, status=status.HTTP_403_FORBIDDEN)
		if tournament.next_match != next_match:
			return Response({'error': f'The next tournament match is not {next_match}'}, status=status.HTTP_403_FORBIDDEN)
		
		try:
			matchup = TournamentMatchup.objects.get(tournament_id=tournament_id, tournament_match_id=next_match)
		except TournamentMatchup.DoesNotExist:
			return Response({'error': f'Could not find tournament matchup [this should not be possible!]'}, status=status.HTTP_404_NOT_FOUND)

		token = MatchTokenManager.create_tournament_match_token(matchup)
		try:
			match = MatchSetupManager.create_match_and_its_players(token)
		except MatchAndPlayersCreationException as e:
			return Response({'error': f'{e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		
		pong_match_url = f'ws://localhost:8080/pong/{match.id}?token={token.token}'
		return Response(pong_match_url, status=status.HTTP_200_OK)
			


