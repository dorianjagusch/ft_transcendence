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
											check_that_valid_tournament_request, \
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

