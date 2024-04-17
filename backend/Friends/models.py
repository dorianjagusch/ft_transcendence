from django.db import models

from UserManagement.models import User

# Create your models here.
class Friends(models.Model):
    # User who initiated the friend request
    user1_id = models.ForeignKey(User, related_name='user1_id', null=False, blank=False, on_delete=models.CASCADE)

    # User who received the friend request
    user2_id = models.ForeignKey(User, related_name='user2_id', null=False, blank=False, on_delete=models.CASCADE)

    # Date and time when the friend relation is set
    start_date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user1_id} - {self.user2_id}"
    
    class Meta:
        # RuntimeError: Model class Friends.models.Friends doesn't declare an explicit app_label and isn't in an application in INSTALLED_APPS
        app_label = 'Friends'

        # prevents a user from having the same relation to another user twice in the table
        unique_together = [['user1_id', 'user2_id'], ['user2_id', 'user1_id']]

