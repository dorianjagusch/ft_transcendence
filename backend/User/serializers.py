from rest_framework import serializers

from .models import User
from Friends.models import Friend
from Friends.mixins import GetFriendshipStatusMixin

class UserInputSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password']

class UserOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'is_online']

class UserFriendOutputSerializer(serializers.ModelSerializer, GetFriendshipStatusMixin):
    friendship = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'is_online', 'friendship']

    def get_friendship(self, obj):
        user_id = self.context['request'].user.id
        friend_id = obj.id
        if not user_id or not friend_id:
            return None
        status = self.get_friendship_status(user_id, friend_id)
        return status
