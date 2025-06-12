from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, MessageHistory, Notification

@receiver(pre_save, sender=Message)
def log_edit(sender, instance, **kwargs):
    if instance.pk:
        original = Message.objects.get(pk=instance.pk)
        if original.content != instance.content:
            instance.edited = True
            MessageHistory.objects.create(
                message=original,
                old_content=original.content
            )

@receiver(post_save, sender=Message)
def notify_user(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(post_delete, sender=User)
def cleanup_on_delete(sender, instance, **kwargs):
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(message__sender=instance).delete()
