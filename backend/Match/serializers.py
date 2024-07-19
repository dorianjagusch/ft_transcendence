from rest_framework import serializers
from .models import Match

class MatchSerializer(serializers.ModelSerializer):
	state_display = serializers.CharField(source='get_state_display', read_only=True)

	class Meta:
		model = Match
		fields = ['id', 'state', 'state_display', 'tournament', 'start_time', 'end_time', 'created_at', 'updated_at']
