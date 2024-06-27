from rest_framework.exceptions import APIException
from rest_framework import status


class TournamentSetupException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'There was an error creating the tournament or its players.'
    default_code = 'tournament_creation_error'

class TournamentInProgressException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'An error occured in the ongoing tournament.'
    default_code = 'tournament_in_progress_error'