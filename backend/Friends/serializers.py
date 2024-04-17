from rest_framework import serializers
from .models import Friends

class FriendsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Friends
		fields = ['id', 'user1_id', 'user2_id', 'start_date_time']
