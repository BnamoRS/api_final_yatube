from rest_framework import permissions


class IsAuthorObjectPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method != permissions.SAFE_METHODS:
            return request.user == obj.author
        #return request.user == obj.author
