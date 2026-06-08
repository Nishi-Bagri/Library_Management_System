from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'ADMIN'
        )
    
class IsAdminOrLibrarian(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.role in [
                'ADMIN',
                'LIBRARIAN'
            ]
        )

class IsLibrarian(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.role == 'LIBRARIAN'
        )

class IsUser(BasePermission):
     
     def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.role == 'USER'
        )
        
        
