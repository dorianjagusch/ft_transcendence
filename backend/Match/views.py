from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from .mixins import GetMatchUrlMixin, GetUserMatchHistoryMixin, GetMatchDetailsMixin
from django.utils.decorators import method_decorator
from shared_utilities.decorators import must_be_authenticated


class MatchView(APIView, GetMatchUrlMixin):
    @method_decorator(must_be_authenticated)
    def get(self, request: Request) -> Response:
        return self.get_match_url(request)

class MatchHistoryView(APIView, GetUserMatchHistoryMixin):
    @method_decorator(must_be_authenticated)
    def get(self, request: Request) -> Response:
        return self.get_user_match_history(request)

class MatchDetailView(APIView, GetMatchDetailsMixin):
    @method_decorator(must_be_authenticated)
    def get(self, request: Request, match_id: int) -> Response:
        return self.get_match_details(match_id)
