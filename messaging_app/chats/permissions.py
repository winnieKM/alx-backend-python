from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsParticipantOfConversation(BasePermission):
    """
    Permission to allow only participants of a conversation to access it.
    """

    def has_permission(self, request, view):
        # Only allow authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS are GET, HEAD, OPTIONS - allow only if participant
        if request.method in SAFE_METHODS:
            return request.user in obj.participants.all()

        # For unsafe methods (POST, PUT, DELETE), allow only if user is participant
        return request.user in obj.participants.all()
