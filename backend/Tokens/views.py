from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from django.utils.decorators import method_decorator

from .serializers import MatchTokenSerializer
from .mixins import CreateSingleMatchTokenMixin, DeactivateMatchToken
from shared_utilities.decorators import must_be_authenticated, valid_serializer_in_body


class SingleMatchGuestTokenView(APIView, CreateSingleMatchTokenMixin, DeactivateMatchToken):
	@method_decorator(must_be_authenticated)
	def post(self, request: Request) -> Response:
		return self.create_single_match_token(request)

	@method_decorator(must_be_authenticated)
	@method_decorator(valid_serializer_in_body(MatchTokenSerializer))
	def put(self, request: Request) -> Response:
		return self.deactivate_match_token(request)
