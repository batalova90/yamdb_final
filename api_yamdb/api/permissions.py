from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if (request.user.is_authenticated
            and request.user.is_admin
                or request.user.is_superuser):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if (request.user.is_authenticated
            and request.user.is_admin
                or request.user.is_superuser):
            return True
        return False


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        if (request.user.is_authenticated
            and request.user.is_moderator
                or request.user.is_staff):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if (request.user.is_authenticated
            and request.user.is_moderator
                or request.user.is_staff):
            return True
        return False


class IsAuthorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if (request.user.is_authenticated
                or request.method in SAFE_METHODS):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if (obj.author == request.user
                or request.method in SAFE_METHODS):
            return True
        return False


class AdminAddInfoClasses(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_admin:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True
        return False
