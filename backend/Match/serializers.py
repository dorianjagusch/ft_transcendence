from rest_framework import serializers
from .models import Match
from Team.models import Team

class MatchSerializer(serializers.ModelSerializer):
	team_1_id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
	team_2_id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())

	# tournament_id = serializers.PrimaryKeyRelatedField(queryset=Tournament.objects.all())
	# tournament_phase_id = serializers.PrimaryKeyRelatedField(queryset=TournamentPhase.objects.all())

	class Meta:
		model = Match
		fields = ['id', 'team_1_id', 'team_2_id']