from rest_framework import serializers

from .models import Tournament, \
                        TournamentPlayer

class TournamentPlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentPlayer
        fields = ['id', 'user', 'name_in_tournament']

