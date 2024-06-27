from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator

from .models import MatchToken, TournamentToken
from .serializers import MatchTokenSerializer, \
							TournamentTokenSerializer, \
							GuestUserAuthSerializer
from User.models import User
from User.serializers import UserInputSerializer, UserOutputSerializer
from Tournament.models import Tournament
from Tournament.serializers import TournamentCreationSerializer
from Tournament.managers import TournamentSetupManager
from Tournament.exceptions import TournamentCreationException

from shared_utilities.decorators import must_be_authenticated, \
											must_not_be_username, \
											valid_serializer_in_body, \
											check_that_valid_tournament_token

# Create your views here.
class SingleMatchGuestTokenView(APIView):
	@method_decorator(must_be_authenticated)
	@method_decorator(must_not_be_username)
	@method_decorator(valid_serializer_in_body(UserInputSerializer))
	def post(self, request):
		host_user = request.user
		username = request.data.get('username')
		password = request.data.get('password')

		guest_user = authenticate(username=username, password=password)
		if guest_user is not None:
			token = MatchToken.objects.create_single_match_token(host_user, guest_user)
			token_serializer = MatchTokenSerializer(token)
			user_serializer = UserOutputSerializer(guest_user)
			return Response({
				'token': token_serializer.data,
				'guest_user': user_serializer.data
			}, status=status.HTTP_201_CREATED)
		else:
			return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

	@method_decorator(must_be_authenticated)
	@method_decorator(valid_serializer_in_body(MatchTokenSerializer))
	def put(self, request):
		try:
			token = MatchToken.objects.get(token=request.data.get('token'))
			if token.is_active == False or token.is_expired():
				token.is_active = False
				token.save()
				return Response({'message': 'Token has already expired'}, status=status.HTTP_200_OK)
			else:
				token.is_active = False
				token.save()
				return Response({'message': 'Token is now expired'}, status=status.HTTP_200_OK)
		except MatchToken.DoesNotExist:
			return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class TournamentTokenView(APIView):
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
				return Response(serializer, status=status.HTTP_201_CREATED)
			except TournamentCreationException as e:
				return Response({'error': str(e)}, status=e.status_code)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TournamentGuestTokenView(APIView):
	@method_decorator(must_be_authenticated)
	@method_decorator(must_not_be_username)
	@method_decorator(valid_serializer_in_body(GuestUserAuthSerializer))
	def post(self, request):
		serializer = GuestUserAuthSerializer(data=request.data, context={'host_user': request.user})
		if serializer.is_valid():
			token = serializer.save()
			token_serializer = TournamentGuestTokenSerializer(token)
			user_serializer = UserOutputSerializer(serializer.validated_data['user'])
			return Response({
				'token': token_serializer.data,
				'guest_user': user_serializer.data
			}, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		
	@method_decorator(must_be_authenticated)
	@method_decorator(must_not_be_username)
	@method_decorator(valid_serializer_in_body(TournamentGuestTokenSerializer))
	def put(self, request):
		try:
			token = TournamentGuestToken.objects.get(token=request.data.get('token'))
			if token.is_active == False or token.is_expired():
				token.is_active = False
				token.save()
				return Response({'message': 'Token has already expired'}, status=status.HTTP_200_OK)
			else:
				token.is_active = False
				token.save()
				return Response({'message': 'Token is now expired'}, status=status.HTTP_200_OK)

		except TournamentGuestToken.DoesNotExist:
			return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
