from rest_framework import permissions


class IsAuthenticatedBusinessUser(permissions.BasePermission):
    message = 'Only Business user has access.'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type == 'business'


class IsAuthenticatedCustomerUser(permissions.BasePermission):
    message = 'Only Customer user has access.'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type == 'customer'

class IsAuthenticatedStaffUser(permissions.BasePermission):
    message = 'Only Staff user can delete order.'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff
