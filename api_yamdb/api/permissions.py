from rest_framework import permissions


class SafeMethodsOnlyPermission(permissions.BasePermission):
    """Права доступа для администратора и при безопасных методах"""

    def has_permission(self, request, view):
        if (request.user.is_superuser or request.method in permissions.SAFE_METHODS):
            return True
        elif request.user.is_authenticated and request.user.is_admin:
            return True
