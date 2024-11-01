from rest_framework.permissions import BasePermission

class NotAuthenticated(BasePermission):
    """
    Custom permission to only allow unauthenticated users to access a view.
    """
    def has_permission(self, request, view):
        return not request.user.is_authenticated