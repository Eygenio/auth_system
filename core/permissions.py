from rest_framework import permissions


class HasPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        # Суперпользователь имеет все права
        if request.user.is_superuser:
            return True

        # Получаем требуемое разрешение из view
        required_permission = getattr(view, 'permission_required', None)
        if not required_permission:
            return True

        # Проверяем наличие разрешения у пользователя
        user_roles = request.user.user_roles.select_related('role').prefetch_related(
            'role__role_permissions__permission')

        for user_role in user_roles:
            for role_permission in user_role.role.role_permissions.all():
                if role_permission.permission.code == required_permission:
                    return True

        return False


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_superuser:
            return True

        # Проверяем, является ли пользователь владельцем объекта
        if hasattr(obj, 'user') and obj.user == request.user:
            return True
        if hasattr(obj, 'owner') and obj.owner == request.user:
            return True

        return False
