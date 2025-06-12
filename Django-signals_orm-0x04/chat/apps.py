from django.apps import AppConfig

class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'

    def ready(self):
        import chat.signals  # Make sure this line is here

class MessagingConfig(AppConfig):
    name = 'messaging'

    def ready(self):
        import messaging.signals