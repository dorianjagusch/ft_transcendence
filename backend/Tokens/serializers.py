from rest_framework import serializers
from .models import AbstractToken, MatchToken

class AbstractTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractToken
        fields = ['token']

class MatchTokenSerializer(AbstractTokenSerializer):
    class Meta(AbstractTokenSerializer.Meta):
        model = MatchToken