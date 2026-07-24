from rest_framework import permissions

class IsAuthenticatedCustomer(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type == 'customer'


class IsAuthenticatedReviewCreator(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.reviewer.id