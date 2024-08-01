from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from .models import Match
from .managers import MatchSetupManager
from .serializers import MatchSerializer
from User.views import User
from Tokens.models import MatchToken
from django.utils.decorators import method_decorator
from shared_utilities.decorators import must_be_authenticated
import sys

class MatchView(APIView):
    @method_decorator(must_be_authenticated)
    def get(self, request):
        token_str = request.query_params.get('token')
        if not token_str or token_str == 'null':
            return Response({"message": "Token parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = MatchToken.objects.get(token=token_str)
        except Exception:
            return Response({"message": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

        if token.already_used_to_get_url == True:
            return Response({"message": "Token already used to get match url."}, status=status.HTTP_403_FORBIDDEN)
        token.already_used_to_get_url = True
        token.save()

        if not token.is_active or token.is_expired():
            return Response({"message": "Expired token."}, status=status.HTTP_403_FORBIDDEN)
        if token.user_left_side.id != request.user.id:
            return Response({"message": "You are not the host user in the token."}, status=status.HTTP_401_UNAUTHORIZED)

        match = MatchSetupManager.create_match_and_its_players(token)

        if not match:
            return Response({"message": "Something went wrong when creating the match and players."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        pong_match_url = f'wss://localhost:8443/pong/{match.id}?token={token.token}'
        return Response(pong_match_url, status=status.HTTP_200_OK)


class MatchHistoryView(APIView):
    @method_decorator(must_be_authenticated)
    def get(self, request):
        user_id = request.query_params.get('user_id')
        user = get_object_or_404(User, pk = user_id)
        if not isinstance(user, User):
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        matches = Match.objects.filter(players__user=user).distinct()
        serializer = MatchSerializer(matches, many = True)
        for match in matches:
            if match.start_ts and timezone.is_naive(match.start_ts):
                match.start_ts = timezone.make_aware(match.start_ts)
            if match.end_ts and timezone.is_naive(match.end_ts):
                match.end_ts = timezone.make_aware(match.end_ts)

        return Response(serializer.data, status=status.HTTP_200_OK)

class MatchDetailView(APIView):
    @method_decorator(must_be_authenticated)
    def get(self, request, match_id):
        return MatchSetupManager.get_match_details(match_id)
