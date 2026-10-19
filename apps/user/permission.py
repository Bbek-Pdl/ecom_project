from rest_framework.permissions import BasePermission


class IsNotAuthenticated(BasePermission):
    def has_permission(self, request, view):
        message = ("Authenticated users cannot register a new account. ")
        if  request.user.is_authenticated:
            self.message = message
            return False
        return True