from rest_framework import permissions


class OwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        print("Permission check is called.")
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
