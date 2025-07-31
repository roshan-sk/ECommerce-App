from rest_framework import permissions
from users.models import UserProfile

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_verified and request.user.is_admin