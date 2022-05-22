from rest_framework import permissions


class SafeMethodsOnlyPermission(permissions.BasePermission):
    """Права доступа для администратора, супрюзера и при безопасных методах"""

    """def has_permission(self, request, view):
        if (request.user.is_superuser
           or request.method in permissions.SAFE_METHODS):
            return True
        elif request.user.is_authenticated and request.user.is_admin:
            return True"""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
            or request.user.is_authenticated and request.user.is_admin
        )


class ReviewsComentsPermission(permissions.BasePermission):
    """Проверка прав доступа для ревью и комментариев"""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
            or request.user.is_admin
            or request.user.is_moderator
            or request.user == obj.author
        )


class AdminOnlyPermission(permissions.BasePermission):
    """Права POST, PATCH, DELETE только администратора, а GET у всех"""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and request.user.is_admin
        )
