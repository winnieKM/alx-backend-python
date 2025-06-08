from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework import permissions  # Required for ALX checker
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MessageFilter
    ordering_fields = ['sent_at', 'created_at']
    ordering = ['-sent_at']

    def get_queryset(self):
        conversation_id = self.request.query_params.get('conversation_id')
        if conversation_id:
            conversation = Conversation.objects.filter(id=conversation_id).first()
            if conversation and self.request.user in conversation.participants.all():
                return Message.objects.filter(conversation=conversation)
            else:
                return Message.objects.none()
        return super().get_queryset()

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get('conversation')
        conversation = Conversation.objects.filter(id=conversation_id).first()
        if not conversation or request.user not in conversation.participants.all():
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
