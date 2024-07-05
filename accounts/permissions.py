from rest_framework import permissions


class IsAuthenticatedParent(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated and is a parent
        return bool(request.user and request.user.is_authenticated and request.user.is_parent)
