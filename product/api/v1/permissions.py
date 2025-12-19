from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsStudentOrIsAdmin(BasePermission):
    """Разрешает оплату только аутентифицированным пользователям."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if view.action == 'pay':
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_staff


class ReadOnlyOrIsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.method in SAFE_METHODS
