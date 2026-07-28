from rest_framework import permissions


class IsAuthenticatedBusinessOwnerUser(permissions.BasePermission):
    """Allow access only to authenticated business users who own the order."""

    message = "Only Business user has access."

    def has_permission(self, request, view):
        """Check user is authenticated and of type business."""

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Check that the business user owns this order."""

        return obj.business_user == request.user


class IsAuthenticatedCustomerUser(permissions.BasePermission):
    """Allow access only to authenticated customer users."""

    message = "Only Customer user has access."

    def has_permission(self, request, view):
        """Check user is authenticated and of type customer."""

        return request.user.is_authenticated and request.user.type == "customer"


class IsAuthenticatedStaffUser(permissions.BasePermission):
    """Allow access only to authenticated staff users."""

    message = "Only Staff user can delete order."

    def has_permission(self, request, view):
        """Check user is authenticated and has staff status."""

        return request.user.is_authenticated and request.user.is_staff