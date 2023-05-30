from rest_framework import permissions


class UserOwnerOrGetAndPost(permissions.BasePermission):
    """
    Permission class to allow access to users objects only if they are owned by the requesting user
    or if the request method is GET or POST.
    """

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            return request.user == obj
        return True


class ProfileOwnerOrGetAndPost(permissions.BasePermission):
    """
    Permission class to allow access to users objects only if they are owned by the requesting user
    or if the request method is GET or POST.
    """

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            return request.user == obj.user
        return True
