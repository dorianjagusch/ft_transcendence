from rest_framework import serializers
from .models import Match

class MatchSerializer(serializers.ModelSerializer):
	state = serializers.CharField(source='get_state_display', read_only=True)

	class Meta:
		model = Match
		fields = ['id', 'state', 'state_display', 'start_ts', 'end_ts', 'insert_ts', 'update_ts']
