import json
from functools import wraps
from django.http import HttpResponseForbidden
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

def must_be_authenticated(view_func):
	@wraps(view_func)
	def wrapper(*args, **kwargs):
		request = args[0] if args else None

		if not request.user.is_authenticated:
			return HttpResponseForbidden("You must be logged in to access this resource.")

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

