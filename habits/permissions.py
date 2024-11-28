from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.autor == request.user


class IsUser(BasePermission):

    def has_object_permission(self, request, view, obj):

        return request.user and request.user == obj
