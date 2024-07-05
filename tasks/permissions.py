from rest_framework.permissions import BasePermission


class IsParent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_parent
