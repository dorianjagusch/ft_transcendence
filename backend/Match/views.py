from functools import partial
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.shortcuts import redirect

from Tokens.models import MatchToken
from Tokens.serializers import MatchTokenSerializer
from shared_utilities.GameSetupManager import GameSetupManager
from django.utils.decorators import method_decorator
from shared_utilities.decorators import must_be_authenticated, \
                                            valid_serializer_in_body

class MatchListView(APIView):
    @method_decorator(must_be_authenticated)
    @method_decorator(valid_serializer_in_body(MatchTokenSerializer))
    def post(self, request):
        token_str = request.data.get('token')
        if not token_str:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = MatchToken.objects.get(token=token_str)
        except MatchToken.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        if not token.is_active or token.is_expired():
            return Response({'error': 'Expired token'}, status=status.HTTP_403_FORBIDDEN)
        if token.user_left_side.id != request.user.id:
            return Response({'error': 'You are not the host user in the token'}, status=status.HTTP_403_FORBIDDEN)

        match, player_left, player_right = GameSetupManager.create_match_and_its_players(token)

        if not all([match, player_left, player_right]):
            return Response({'error': 'Something went wrong when creating the match and players'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        pong_match_url = f'ws://localhost:8080/pong/{match.id}'
        return Response(pong_match_url, status=status.HTTP_200_OK)


class LaunchTestMatchView(APIView):
	@method_decorator(must_be_authenticated)
	def get(self, request):
		token = MatchToken.objects.create_single_match_token(request.user, request.user)
		match, player_left_side, player_right_side = GameSetupManager.create_match_and_its_players(token)
		if not all([match, player_left_side, player_right_side]):
			return Response({'error': 'Something went wrong when creating the match and players'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		
		pong_match_url = f'ws://localhost:8080/pong/{match.id}'
		return Response(pong_match_url, status=status.HTTP_200_OK)