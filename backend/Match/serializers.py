from rest_framework import serializers
from .models import Match

class MatchSerializer(serializers.ModelSerializer):
	state = serializers.CharField(source='get_state_display', read_only=True)

	class Meta:
		model = Match
		fields = ['id', 'state', 'start_ts', 'end_ts', 'duration']

