from rest_framework import serializers

from .models import Tournament, \
                        TournamentParticipant, \
                        TournamentMatchup
from Tokens.models import TournamentGuestToken

class TournamentParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentParticipant
        fields = ['id', 'user', 'name_in_tournament']

class TournamentMatchupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentMatchup
        fields = ['id', 'tournament_match_id', 'player1', 'player2', 'winner']

class TournamentOutputSerializer(serializers.ModelSerializer):
    state_display = serializers.CharField(source='get_state_display', read_only=True)
    participants = TournamentParticipantSerializer(many=True, read_only=True)
    matchups = TournamentMatchupSerializer(many=True, read_only=True)

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
            'tournament_winner',
            'insert_ts',
            'start_ts',
            'end_ts',
            'updated_ts',
            'participants',
            'matchups'
            ]

class TournamentCreationSerializer(serializers.ModelSerializer):
    tokens = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True
    )
    host_user_custom_name = serializers.CharField(required=False, allow_blank=True, allow_null=True) # this name stuff is a bit sus...
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


