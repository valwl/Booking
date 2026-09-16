from rest_framework import permissions
from rest_framework.permissions import BasePermission

from booking.models.booking import Booking


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user



