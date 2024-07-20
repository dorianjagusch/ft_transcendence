from django.db import models
import uuid
from datetime import timedelta
from django.utils import timezone
from .managers import MatchTokenManager

from User.models import User

class AbstractToken(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=5)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return str(self.token)

class MatchToken(AbstractToken):
    user_left_side = models.ForeignKey(User, related_name='match_token_left', on_delete=models.CASCADE)
    user_right_side = models.ForeignKey(User, related_name='match_token_right', null=True, on_delete=models.CASCADE)

    objects = MatchTokenManager()
