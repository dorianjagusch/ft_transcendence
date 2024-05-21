from rest_framework import serializers
from .models import Player
from Match.models import Match
from User.models import User

class PlayerSerializer(serializers.ModelSerializer):
	user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
	match_id = serializers.PrimaryKeyRelatedField(queryset=Match.objects.all())

	class Meta:
		model = Player
		fields = ['id', 'user_id', 'match_id', 'score', 'match_winner']