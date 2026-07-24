from rest_framework import permissions


class IsAuthenticatedCustomer(permissions.BasePermission):
    """Allow access only to authenticated customer users."""

    def has_permission(self, request, view):
        """Check user is authenticated and of type customer."""

        return request.user.is_authenticated and request.user.type == "customer"


class IsAuthenticatedReviewCreator(permissions.BasePermission):
    """Allow write access only to the creator of the review."""

    def has_permission(self, request, view):
        """Check user is authenticated."""

        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Check that the requesting user is the review creator."""

        return request.user.id == obj.reviewer.id