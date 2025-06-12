from django.db import models

class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        return self.filter(receiver=user, read=False)

from .managers import UnreadMessagesManager

class Message(models.Model):
    # ...fields
    unread = UnreadMessagesManager()
