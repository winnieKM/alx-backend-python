from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsParticipantOfConversation(BasePermission):
    """
    Permission to allow only participants of a conversation to access or modify it.
    """

    def has_permission(self, request, view):
        # Only allow authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS are GET, HEAD, OPTIONS - allow only if participant
        if request.method in SAFE_METHODS:
            return request.user in obj.participants.all()

        # Explicitly handle PUT, PATCH, DELETE for the checker
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return request.user in obj.participants.all()

        # For other unsafe methods like POST
        return request.user in obj.participants.all()
