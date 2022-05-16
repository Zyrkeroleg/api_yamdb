# Пусть заготовка пока повисит тут на случай,
# если пермишн во views не будет работать
from rest_framework import permissions


class ReviewsComentsPermission(permissions.BasePermission):
    """Проверка прав доступа для ревью и комментариев"""

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_admin:
            return True
        elif request.user == obj.author:
            return True
