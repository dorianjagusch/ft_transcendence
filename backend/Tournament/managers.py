from django.db import transaction

from .models import Tournament, \
                        TournamentPlayer
from .serializers import TournamentCreationSerializer
from .exceptions import TournamentSetupException
from User.models import User

class TournamentSetupManager:
    @staticmethod
    def create_tournament_and_tournament_player_for_host(validated_data: TournamentCreationSerializer.validated_data):
        try:
            with transaction.atomic():
                tournament = Tournament.objects.create(
                    name=validated_data['name'] if validated_data['name'] else None,
                    host_user=validated_data['host_user'],
                    player_amount=validated_data['player_amount']
                )

                TournamentPlayer.objects.create(
                    tournament=tournament,
                    user=tournament.host_user,
                    display_name=validated_data['host_user_display_name'] if validated_data['host_user_display_name'] else None
                )

                return tournament

        except Exception as e:
            return TournamentSetupException(e)

class TournamentInProgressManager:
    pass