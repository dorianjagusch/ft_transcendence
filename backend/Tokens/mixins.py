from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from .models import MatchToken
from .serializers import MatchTokenSerializer
from User.models import User
from User.serializers import UserOutputSerializer
from User.mixins import AuthenticateUserMixin
from Match.models import Match


# used in CreateSingleMatchTokenMixin and CreateTournamentMatchTokenMixin
def create_match_token(user_left_side: User, user_right_side: User | None) -> MatchToken:
	match_token = MatchToken.objects.create(
		user_left_side=user_left_side,
		user_right_side=user_right_side
	)
	return match_token

class CreateSingleMatchTokenMixin(AuthenticateUserMixin):
	"""
	Mixin for creating a token for a single match.
	Creates a token for either a guest or an AI match based on the request.
	"""
	def create_single_match_token(self, request: Request) -> Response:
		host_user = request.user
		ai_opponent = request.query_params.get('ai_opponent')
		if ai_opponent is not None and ai_opponent == 'true':
			token = create_match_token(host_user, None)
			token_serializer = MatchTokenSerializer(token)
			return Response({
				'token': token_serializer.data,
			}, status=status.HTTP_201_CREATED)

		result = self.authenticate_user(request)
		if not isinstance(result, User):
			response = result
			return response
		
		user = result
		if user == host_user:
			return Response({"message": "You cannot play against yourself."}, status=status.HTTP_403_FORBIDDEN)

		token = create_match_token(host_user, user)
		token_serializer = MatchTokenSerializer(token)
		user_serializer = UserOutputSerializer(user)
		return Response({
			'token': token_serializer.data,
			'guest_user': user_serializer.data
		}, status=status.HTTP_201_CREATED)

class DeactivateMatchToken:
	"""
	Mixin for deactivating match token.
	"""
	def deactivate_match_token(self, request: Request) -> Response:
		try:
			token = MatchToken.objects.get(token=request.data.get('token'))
			if token.is_active == False or token.is_expired():
				token.is_active = False
				token.save()
				return Response({"message": "Token has already expired."}, status=status.HTTP_200_OK)
			else:
				token.is_active = False
				token.save()
				return Response({"message": "Token is now expired."}, status=status.HTTP_200_OK)
		except Exception:
			return Response({"message": "Token was not found."}, status=status.HTTP_400_BAD_REQUEST)

class CreateTournamentMatchTokenMixin:
	"""
	Mixin for creating a token for a tournament match.
	"""
	def create_tournament_match_token(self, match: Match) -> MatchToken:
		players = match.players.all()
		return create_match_token(players[0].user, players[1].user)
