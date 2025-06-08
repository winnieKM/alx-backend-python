from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to allow only participants of a conversation to 
    send, view, update (PATCH), or delete messages.
    """

    def has_permission(self, request, view):
        # Only allow authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # If obj is a Conversation
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        # If obj is a Message, check the conversation's participants
        if hasattr(obj, 'conversation') and hasattr(obj.conversation, 'participants'):
            if request.method in SAFE_METHODS or request.method in ['PATCH', 'DELETE']:
                return request.user in obj.conversation.participants.all()

        # Default fallback
        return False
