from rest_framework.exceptions import APIException
from rest_framework import status


class MatchAndPlayersCreationException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'There was an error when creating the match and/or players.'
    default_code = 'match_and_players_creation_error'

class MatchPlayersException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'There was an error involving match players.'
    default_code = 'match_players_error'
