from rest_framework import permissions


class SafeMethodsOnlyPermission(permissions.BasePermission):
    """Права доступа для администратора и при безопасных методах"""

    def has_permission(self, request, view):
        if (request.user.is_superuser
                or request.method in permissions.SAFE_METHODS):
            return True
        elif request.user.is_authenticated and request.user.is_admin:
            return True


# Пусть заготовка пока повисит тут на случай,
# если пермишн во views не будет работать
class ReviewsComentsPermission(permissions.BasePermission):
    """Проверка прав доступа для ревью и комментариев"""

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_admin:
            return True
        elif (request.user == obj.author
              or request.method in permissions.SAFE_METHODS):
            return True
