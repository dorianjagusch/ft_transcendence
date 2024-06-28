import json
from functools import wraps
from datetime import timezone
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.request import Request
from django.http import HttpResponseForbidden, \
							HttpResponseNotFound

from Tournament.models import Tournament, \
								TournamentPlayer
from Tournament.tournamentState import TournamentState

from rest_framework.validators import UniqueValidator, \
										UniqueTogetherValidator

def must_be_authenticated(view_func):
	@wraps(view_func)
	def wrapper(*args, **kwargs):
		request = args[0] if args else None

		if not request.user.is_authenticated:
			return Response({'message': "Please log in to access this resource.",'error': "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
		return view_func(*args, **kwargs)
	return wrapper

def must_be_url_user(view_func):
	@wraps(view_func)
	def wrapper(*args, **kwargs):
		request = args[0] if args else None

		if request.user.is_superuser:
			return view_func(*args, **kwargs)

		object_owner_id = kwargs.get('user_id')  # URL parameter
		if request.user.id != object_owner_id:
			return HttpResponseForbidden("You are not authorized to modify this resource.")

		return view_func(*args, **kwargs)
	return wrapper


def must_be_body_user_id(view_func):
	@wraps(view_func)
	def wrapper(*args, **kwargs):
		request = args[0] if args else None

		try:
			user_id = request.data.get('user_id')
		except KeyError:
			return HttpResponseForbidden("Missing 'user_id' in request data.")

		if request.user.is_superuser:
			return view_func(*args, **kwargs)

		if request.user.id != user_id:
			return HttpResponseForbidden("You are not authorized to modify this resource.")

		return view_func(*args, **kwargs)
	return wrapper


def valid_serializer_in_body(serializer_class, **kwargs):
	def decorator(view_func):
		@wraps(view_func)
		def wrapper(*args, **kwargs):
			request = args[0] if args else None

			class IgnoreUniqueConstraintsSerializer(serializer_class):
				def __init__(self, *args, **kwargs):
					super().__init__(*args, **kwargs)
					self.remove_unique_validators()

				def remove_unique_validators(self):
					for field_name, field in self.fields.items():
						field.validators = [v for v in field.validators if not isinstance(v, UniqueValidator)]
					self.validators = [v for v in self.validators if not isinstance(v, UniqueTogetherValidator)]

			serialized_data = request.data
			serializer = IgnoreUniqueConstraintsSerializer(data=serialized_data, **kwargs)
			try:
				serializer.is_valid(raise_exception=True)
				return view_func(*args, **kwargs)
			except serializers.ValidationError as e:
				return Response({'message': "Non-valid JSON object in request body.",'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

		return wrapper
	return decorator

# Used with GuestUserAuthenticationView to prevent the host user from authenticating themself
def must_not_be_username(view_func):
	@wraps(view_func)
	def wrapper(*args, **kwargs):
		request = args[0] if args else None

		try:
			username = request.data.get('username')
		except KeyError:
			return HttpResponseForbidden("Missing 'username' in request data.")

		if request.user.is_superuser:
			return view_func(*args, **kwargs)

		if request.user.username == username:
			return HttpResponseForbidden("request data username has to be different from the logged in user's username.")

		return view_func(*args, **kwargs)
	return wrapper

def check_that_valid_tournament_lobby_request(view_func):
	'''Check that a request that modifies tournament resource is valid.

	The user making the request must be the tournament host.
	The tournament state must be in lobby.
	The tournament cannot be expired. If it is, set state to aborted.
	'''
	@wraps(view_func)
	def wrapper(*args, **kwargs):
		request = args[0] if args else None

		if request.user.is_superuser:
			return view_func(*args, **kwargs)

		tournament_id = kwargs.get('tournament_id', None)
		tournament = Tournament.objects.filter(id=tournament_id).first()
		if not tournament:
			return HttpResponseNotFound(f"Tournament {tournament_id} does not exist.")

		if request.user != tournament.host_user:
			return HttpResponseForbidden("You are not authorized to modify this resource.")

		if tournament.state != TournamentState.LOBBY:
			return HttpResponseForbidden("Cannot modify this resource because tournament is not in lobby.")
		
		if timezone() > tournament.expires_ts:
			tournament.state=TournamentState.ABORTED
			tournament.save()
			return HttpResponseForbidden("Tournament has expired; tournament set to aborted!")


		return view_func(*args, **kwargs)
	return wrapper

def check_that_valid_tournament_in_progress_request(view_func):
	'''Check that a request that modifies tournament resource is valid.

	The user making the request must be the tournament host.
	The tournament state must be in progress.
	The tournament cannot be expired. If it is, set state to aborted.
	'''
	@wraps(view_func)
	def wrapper(*args, **kwargs):
		request = args[0] if args else None

		if request.user.is_superuser:
			return view_func(*args, **kwargs)

		tournament_id = kwargs.get('tournament_id', None)
		tournament = Tournament.objects.filter(id=tournament_id).first()
		if not tournament:
			return HttpResponseNotFound(f"Tournament {tournament_id} does not exist.")

		if request.user != tournament.host_user:
			return HttpResponseForbidden("You are not authorized to modify this resource.")

		if tournament.state != TournamentState.IN_PROGRESS:
			return HttpResponseForbidden("Cannot modify this resource because tournament is not in progress.")
		
		if timezone() > tournament.expires_ts:
			tournament.state=TournamentState.ABORTED
			tournament.save()
			return HttpResponseForbidden("Tournament has expired; tournament set to aborted!")


		return view_func(*args, **kwargs)
	return wrapper

def check_that_tournament_players_are_still_active(view_func):
	'''Check that all tournament players that are taking part in tournament are still active.
	If not, abort tournament.

	Use only with POST, PUT or DELETE requests that have to do with active tournaments.
	Always use after check_that_valid_tournament_request decorator!
	'''
	@wraps(view_func)
	def wrapper(*args, **kwargs):
		request = args[0] if args else None

		if request.user.is_superuser:
			return view_func(*args, **kwargs)

		tournament_id = kwargs.get('tournament_id', None)
		tournament = Tournament.objects.filter(id=tournament_id).first()
		if not tournament:
			return HttpResponseNotFound(f"Tournament {tournament_id} does not exist.")

		inactive_players = tournament.players.filter(user__is_active=False)
		if inactive_players.exists():
			tournament.state = TournamentState.ABORTED
			tournament.save()
			return HttpResponseNotFound("One or more users taking part in tournament have deleted their profile; tournament aborted!")

		return view_func(*args, **kwargs)
	return wrapper

