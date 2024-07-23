from functools import partial
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.shortcuts import redirect, get_object_or_404
import sys

from .managers import MatchSetupManager
from .serializers import MatchSerializer
from User.views import User
from Tokens.models import MatchToken
from Tokens.managers import MatchTokenManager
from django.utils.decorators import method_decorator
from shared_utilities.decorators import must_be_authenticated

class MatchView(APIView):
    @method_decorator(must_be_authenticated)
    def get(self, request):
        token_str = request.query_params.get('token')
        if not token_str:
            return Response({'error': 'Token parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = MatchToken.objects.get(token=token_str)
        except MatchToken.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        if not token.is_active or token.is_expired():
            return Response({'error': 'Expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        if token.user_left_side.id != request.user.id:
            return Response({'error': 'You are not the host user in the token'}, status=status.HTTP_403_FORBIDDEN)

        match = MatchSetupManager.create_match_and_its_players(token)

        if not match:
            return Response({'error': 'Something went wrong when creating the match and players'}, status=status.HTTP_403_FORBIDDEN)

        pong_match_url = f'ws://localhost:8080/pong/{match.id}?token={token.token}'
        return Response(pong_match_url, status=status.HTTP_200_OK)


class LaunchTestMatchView(APIView):
	@method_decorator(must_be_authenticated)
	def get(self, request):
		token = MatchTokenManager.create_single_match_token(request.user, request.user)
		match = MatchSetupManager.create_match_and_its_players(token)
		if not match:
			return Response({'error': 'Something went wrong when creating the match and players'}, status=status.HTTP_403_FORBIDDEN)

		pong_match_url = f'ws://localhost:8080/pong/{match.id}?token={token.token}'
		return Response(pong_match_url, status=status.HTTP_200_OK)
     
class MatchHistory(APIView):
     def get(self, request):
        user_id = request.query_params.get('user_id')
        user = get_object_or_404(User, pk = user_id)
        if not isinstance(user, User):
            return Response({"message": "User not found"})
        player_instances = user.players.all()
        matches = [player.match for player in player_instances]
        print (matches, file=sys.stderr)
        serializer = MatchSerializer(matches, many = True)

        return Response(serializer.data, status=status.HTTP_200_OK)