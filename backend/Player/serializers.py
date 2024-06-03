from rest_framework import serializers
from .models import Player
from Match.models import Match
from User.models import User

class PlayerSerializer(serializers.ModelSerializer):
	user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
	match = serializers.PrimaryKeyRelatedField(queryset=Match.objects.all())

	class Meta:
		model = Player
		fields = ['id', 'user', 'match', 'score', 'match_winner']