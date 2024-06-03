from rest_framework import serializers
from .models import AbstractToken, MatchToken, TournamentGuestToken

class AbstractTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractToken
        fields = ['token']

class MatchTokenSerializer(AbstractTokenSerializer):
    class Meta(AbstractTokenSerializer.Meta):
        model = MatchToken

class TournamentGuestTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentGuestToken