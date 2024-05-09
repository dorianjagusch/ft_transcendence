from django.db import models

from User.models import User

class FriendsManager(models.Manager):
    def get_user_friends(self, user_id):
        user_friends = self.filter(user_id=user_id).values_list('friend_id', flat=True)
        friends_of_user = self.filter(friend_id=user_id).values_list('user_id', flat=True)
        actual_user_friends = set(user_friends) & set(friends_of_user)

        friends = User.objects.filter(id__in=actual_user_friends)
        return friends
    
    def get_friendship_by_user_and_friend_id(self, user_id, friend_id):
        return self.get(user_id=user_id, friend_id=friend_id)
    
    def get_friendship_by_id(self, friendship_id):
        return self.get(id=friendship_id)

    def create_friendship(self, user_id, friend_id):
        return self.create(user_id=user_id, friend_id=friend_id)

