from rest_framework import permissions


class IsBusinessUser(permissions.BasePermission):
    """Allow access only to authenticated business users."""

    message = 'Action only allowed for user of type "business".'

    def has_permission(self, request, view):
        """Check user is authenticated and of type business."""

        return request.user.is_authenticated and request.user.type == "business"


class IsOfferOwner(permissions.BasePermission):
    """Allow access only to the owner of the offer."""

    message = "Action only allowed for offer owner."

    def has_permission(self, request, view):
        """Require authentication before checking object ownership."""

        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Check the requesting user owns the offer."""

        return request.user == obj.user