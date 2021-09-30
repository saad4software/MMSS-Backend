from rest_framework import permissions
from .models import User


class IsCounter(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and \
               (request.user.role == 'C' or request.user.role == 'A')


class IsGuest(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and \
               (request.user.role == 'G' or request.user.role == 'C' or request.user.role == 'A')


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and request.user.role == 'A'
