from rest_framework.permissions import BasePermission

class IsCustomer(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'customer'

class IsCourier(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'courier'

class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'
