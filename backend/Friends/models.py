from django.db import models

from User.models import User

# Create your models here.
class Friends(models.Model):
    # User who initiated the friend request
    user_id = models.ForeignKey(User, related_name='user_id', null=False, blank=False, on_delete=models.CASCADE)

    # User who received the friend request
    friend_id = models.ForeignKey(User, related_name='friend_id', null=False, blank=False, on_delete=models.CASCADE)

    # Date and time when the friend request is sent
    insertTS = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} - {self.friend_id} - {self.insertTS}"
    
    class Meta:
        # required because of RunTimeError that complains about lack of app_label
        app_label = 'Friends'

        # prevents a user from having the same relation to another user twice in the table
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'friend_id'], name='unique_user_friend_pair')
        ]

