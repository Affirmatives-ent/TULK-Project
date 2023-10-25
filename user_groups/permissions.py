from rest_framework.permissions import BasePermission


class IsGroupAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user making the request is the creator of the group
        return obj.creator == request.user


class IsAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user is an admin of the group
        return obj.admin == request.user
