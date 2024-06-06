from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator

from .models import Tournament, TournamentState
from .serializers import TournamentOutputSerializer, \
							TournamentCreationSerializer
from .managers import TournamentSetupManager, \
						TournamentInProgressManager
from .exceptions import TournamentCreationException

from shared_utilities.decorators import must_be_authenticated

@method_decorator(must_be_authenticated)
class StartTournamentView(APIView):
	def post(self, request):
		serializer = TournamentCreationSerializer(data=request.data, context={'request': request})
		if serializer.is_valid():
			validated_data = serializer.validated_data
			try:
				tournament = TournamentSetupManager.create_tournament_and_its_players(validated_data)
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

		serializer = TournamentOutputSerializer(tournament)
		return Response(serializer.data)

