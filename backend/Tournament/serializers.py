from rest_framework import serializers

from .models import Tournament, \
                        TournamentPlayer
from Tokens.models import TournamentGuestToken
from Match.models import Match
from Player.models import Player

class TournamentPlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentPlayer
        fields = ['user', 'name_in_tournament']


class TournamentMatchSerializer(serializers.ModelSerializer):
    first_tournament_player = serializers.SerializerMethodField()
    second_tournament_player = serializers.SerializerMethodField()
    class Meta:
        model = Match
        fields = ['id', 'tournament_match_id', 'first_tournament_player', 'second_tournament_player']

    def get_first_tournament_player(self, obj):
        first_player = obj.players.first()
        if first_player:
            tournament_player = TournamentPlayer.objects.filter(
                tournament=obj.tournament,
                user=first_player.user
            ).first()
            return TournamentPlayerSerializer(tournament_player).data if tournament_player else None
        return None

    def get_second_tournament_player(self, obj):
        second_player = obj.players.all()[1] if obj.players.count() > 1 else None
        if second_player:
            tournament_player = TournamentPlayer.objects.filter(
                tournament=obj.tournament,
                user=second_player.user
            ).first()
            return TournamentPlayerSerializer(tournament_player).data if tournament_player else None
        return None


class TournamentOutputSerializer(serializers.ModelSerializer):
    state_display = serializers.CharField(source='get_state_display', read_only=True)
    tournament_players = TournamentPlayerSerializer(many=True, read_only=True)
    matches = TournamentMatchSerializer(many=True, read_only=True)

    class Meta:
        model = Tournament
        fields = [
            'id',
            'host_user',
            'custom_name',
            'state',
            'state_display',
            'next_match',
            'player_amount',
            'winner',
            'insert_ts',
            'start_ts',
            'end_ts',
            'updated_ts',
            'expires_ts',
            'tournament_players',
            'matches'
            ]

class TournamentCreationSerializer(serializers.ModelSerializer):
    tokens = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True
    )
    host_user_custom_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    custom_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Tournament
        fields = [
            'custom_name',
            'host_user',
            'host_user_custom_name',
            'player_amount',
            'tokens'
        ]
        read_only_fields = ['state', 'start_time', 'end_time', 'updated_at']

    def validate_custom_name(self, value):
        if value is None or value == '':
            raise serializers.ValidationError("This field may not be blank or null.")
        if len(value) > 30:
            raise serializers.ValidationError("Ensure this field has no more than 30 characters.")
        return value

    def validate_tournament_guest_token(self, token):
        try:
            guest_token = TournamentGuestToken.objects.get(token=token)
        except TournamentGuestToken.DoesNotExist:
            raise serializers.ValidationError(f'Token {token} does not exist')

        if not guest_token.is_active:
            raise serializers.ValidationError(f'Token {token} is not active')
        if guest_token.is_expired():
            raise serializers.ValidationError(f'Token {token} is expired')
        if self.context['request'].user != guest_token.host_user:
            raise serializers.ValidationError('You are not the host user for this token')
        
        return guest_token

    def validate_token_amount(self, tokens):
        tokens_amount = len(tokens)
        if tokens_amount not in [3, 7]:
            raise serializers.ValidationError("There must be 3 or 7 guest tokens.")
        
    def validate(self, data):
        custom_name = data.get('custom_name')
        if custom_name:
            self.validate_custom_name(custom_name)

        host_user_custom_name = data.get('host_user_custom_name')
        if host_user_custom_name:
            self.validate_custom_name(host_user_custom_name)

        guest_tokens = data.get('tokens')
        if not guest_tokens:
            raise serializers.ValidationError("No tokens in serializer.")
        
        self.validate_token_amount(guest_tokens)

        # Validate each token
        validated_tokens = [self.validate_tournament_guest_token(token) for token in guest_tokens]

        # Update data with validated tokens
        data['tokens'] = validated_tokens

        return data

class TournamentInProgressSerializer(serializers.ModelSerializer):
    state_display = serializers.CharField(source='get_state_display', read_only=True)
    participants = TournamentPlayerSerializer(many=True, read_only=True)
    matches = TournamentMatchSerializer(many=True, read_only=True)
    next_match = serializers.SerializerMethodField()

    class Meta:
        model = Tournament
        fields = [
            'id',
            'host_user',
            'custom_name',
            'state',
            'state_display',
            'expires_ts',
            'player_amount',
            'participants',
            'matches',
            'next_match',
        ]
        
    def get_next_match(self, obj):
        next_match = obj.next_match
        try:
            next_match = Match.objects.get(tournament=obj, tournament_match_id=next_match)
            return TournamentMatchSerializer(next_match).data
        except Match.DoesNotExist:
            return None
