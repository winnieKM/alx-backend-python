from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User model extending AbstractUser to add extra fields if needed
class User(AbstractUser):
    # Add extra fields here if needed, for now we keep it simple
    pass

# Conversation model - tracks users involved in conversation
class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"

# Message model - a message sent by a user inside a conversation
class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='messages_sent', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.id} by {self.sender.username}"
