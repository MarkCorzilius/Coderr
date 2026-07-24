from rest_framework import permissions


class IsProfileOwner(permissions.BasePermission):
    """Allow write access only to the profile owner."""

    def has_object_permission(self, request, view, obj):
        """Check that the requesting user owns this profile."""

        return request.user == obj.user