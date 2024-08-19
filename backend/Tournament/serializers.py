from rest_framework import serializers

from .models import Tournament, TournamentPlayer
from Match.models import Match
from Match.matchState import MatchState

class TournamentSerializer(serializers.ModelSerializer):
	state_display = serializers.CharField(source='get_state_display', read_only=True)

	class Meta:
		model = Tournament
		fields = ['id', 'name', 'state_display', 'player_amount']


class TournamentPlayerSerializer(serializers.ModelSerializer):
	class Meta:
		model = TournamentPlayer
		fields = ['id', 'user', 'display_name']


class TournamentMatchSerializer(serializers.ModelSerializer):
	tournament_match_id = serializers.SerializerMethodField()
	state = serializers.CharField(source='get_state_display', read_only=True)
	tournament_player_left = serializers.SerializerMethodField()
	tournament_player_right = serializers.SerializerMethodField()
	winner = serializers.SerializerMethodField()
	class Meta:
		model = Match
		fields = ['tournament_match_id', 'id', 'state', 'tournament_player_left', 'tournament_player_right', 'winner']

	def get_tournament_match_id(self, match: Match) -> int:
		matches = match.tournament.matches.all().order_by('id')
		match_ids = list(matches.values_list('id', flat=True))
		return match_ids.index(match.id)

	def get_tournament_player_left(self, match: Match) -> TournamentPlayerSerializer | None:
		first_player = match.players.first()
		if first_player:
			tournament_player = TournamentPlayer.objects.filter(
				tournament=match.tournament,
				user=first_player.user
			).first()
			return TournamentPlayerSerializer(tournament_player).data if tournament_player else None
		return None

	def get_tournament_player_right(self, match: Match) -> TournamentPlayerSerializer | None:
		second_player = match.players.all()[1] if match.players.count() > 1 else None
		if second_player:
			tournament_player = TournamentPlayer.objects.filter(
				tournament=match.tournament,
				user=second_player.user
			).first()
			return TournamentPlayerSerializer(tournament_player).data if tournament_player else None
		return None

	def get_winner(self, match: Match) -> TournamentPlayerSerializer | None:
		if match.state == MatchState.FINISHED:
			winning_player = match.players.filter(match_winner=True).first()
			if winning_player:
				winning_tournament_player = TournamentPlayer.objects.filter(
					tournament=match.tournament,
					user=winning_player.user
				).first()
				return TournamentPlayerSerializer(winning_tournament_player).data if winning_tournament_player else None
		return None


class TournamentCreationSerializer(serializers.ModelSerializer):
	host_user_display_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)

	class Meta:
		model = Tournament
		fields = [
			'name',
			'host_user',
			'host_user_display_name',
			'player_amount',
		]

	def validate_custom_name(self, custom_name: str) -> str:
		if custom_name == '':
			raise serializers.ValidationError("This field may not be blank.")
		if len(custom_name) > 30:
			raise serializers.ValidationError("Ensure this field has no more than 30 characters.")
		return custom_name

	def validate_tournament_player_amount(self, player_amount: int) -> None:
		if player_amount not in [4, 8]:
			raise serializers.ValidationError("Must have 4 or 8 players.")

	def validate(self, data):
		tournament_name = data.get('name')
		if tournament_name:
			self.validate_custom_name(tournament_name)
		# TODO: hostname should suffice
		host_user_display_name = data.get('host_user_display_name')
		if host_user_display_name:
			self.validate_custom_name(host_user_display_name)

		self.validate_tournament_player_amount(data.get('player_amount'))

		return data


class TournamentInProgressSerializer(serializers.ModelSerializer):
	state = serializers.CharField(source='get_state_display', read_only=True)

	class Meta:
		model = Tournament
		fields = [
			'id',
			'host_user',
			'name',
			'state',
			'expire_ts',
			'player_amount',
			'next_match',
		]


class TournamentSerializers:
	default = TournamentSerializer
	creation = TournamentCreationSerializer
	in_progress = TournamentInProgressSerializer
	player = TournamentPlayerSerializer
	match = TournamentMatchSerializer