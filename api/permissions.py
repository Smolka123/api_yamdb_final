from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
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
