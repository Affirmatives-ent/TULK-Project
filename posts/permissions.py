from rest_framework import permissions


class IsOwnerOrSuperuserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow read permissions to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the user is the owner of the post
        if obj.author == request.user:
            return True

        # Check if the user is a superuser
        if request.user.is_superuser:
            return True

        return False
