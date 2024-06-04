from rest_framework import serializers
from .models import User

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

	def __init__(self, *args, **kwargs):
		self.friendship = kwargs.pop('friendship', None)
		super().__init__(*args, **kwargs)

	def get_friendship(self, obj):
			return self.friendship
