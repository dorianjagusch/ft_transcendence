from rest_framework import serializers
from .models import User
from Friends.managers import FriendsManager
from Friends.models import Friend

class UserInputSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)

	class Meta:
		model = User
		fields = ['id', 'username', 'password']

class UserOutputSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'username', 'is_online']


class UserFriendOutputSerializer(serializers.ModelSerializer):
	friendship = serializers.SerializerMethodField()

	class Meta:
		model = User
		fields = ['id', 'username', 'is_online', 'friendship']

	def get_friendship(self, obj):
		user_id = self.context['request'].user.id
		friend_id = obj.id
		if (not user_id or not friend_id):
			return None
		status = FriendsManager.get_friendship_status(Friend.objects, user_id, friend_id)
		return status
