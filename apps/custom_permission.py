from rest_framework.permissions import BasePermission


class NoPermission(BasePermission):
    """
    没有任何权限
    """

    def has_permission(self, request, view):
        return False
