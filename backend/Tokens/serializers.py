from rest_framework import serializers
from .models import AbstractToken, AuthenticatedGuestUserToken

class AbstractTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractToken
        fields = ['token']


class AuthenticatedGuestUserTokenSerializer(AbstractTokenSerializer):
    class Meta(AbstractTokenSerializer.Meta):
        model = AuthenticatedGuestUserToken
