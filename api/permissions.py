from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return (request.user.is_staff
                    or request.user.role == request.user.UserRoles.ADMIN)


class IsAdmin(permissions.BasePermission):
    """
    Administrator access rights.
    is_staff - Indicates whether the user has access to the admin interface.
    (SuperuserDjango & AdminUser)
    Or whether the Administrator role is installed (model).
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.is_staff or
                    request.user.role == request.user.UserRoles.ADMIN)
