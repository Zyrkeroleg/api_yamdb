from rest_framework import permissions


class AdminOnlyPermission(permissions.BasePermission):
    """Права доступа строго только администратора."""

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        elif request.user.is_authenticated and request.user.is_admin:
            return True
