from rest_framework import permissions

class IsBusinessUser(permissions.BasePermission):
    message = 'Action only allowed for user of type "business".'

    def has_permission(self, request, view):
        return (
        request.user.is_authenticated and
        request.user.type == 'business'
        )


class IsOfferOwner(permissions.BasePermission):
    message = 'Action only allowed for offer owner.'

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user