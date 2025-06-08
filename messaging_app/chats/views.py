from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter

class MessageViewSet(viewsets.ModelViewSet):
    """
    Handles sending, viewing, updating, and deleting messages.
    Only participants of the conversation can access these messages.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MessageFilter
    ordering_fields = ['sent_at', 'created_at']
    ordering = ['-sent_at']

    def get_queryset(self):
        """
        Filters messages to only those within a conversation the user is part of.
        """
        conversation_id = self.request.query_params.get('conversation_id')
        if conversation_id:
            try:
                conversation = Conversation.objects.get(id=conversation_id)
                if self.request.user in conversation.participants.all():
                    return Message.objects.filter(conversation=conversation)
                else:
                    # Forbidden if user is not a participant
                    return Message.objects.none()
            except Conversation.DoesNotExist:
                return Message.objects.none()
        return Message.objects.none()


class ConversationViewSet(viewsets.ModelViewSet):
    """
    Handles viewing and creating conversations.
    Only participants can access their conversations.
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        """
        Returns conversations the current user is a participant in.
        """
        return Conversation.objects.filter(participants=self.request.user)
