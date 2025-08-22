from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsInOrganization(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request, 'organization', None))

class HasRole(BasePermission):
    required_roles = None

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated and request.organization):
            return False
        roles = set(r.role for r in request.user.memberships.filter(organization=request.organization))
        return bool(self.required_roles and roles.intersection(self.required_roles))

class IsAdmin(HasRole):
    required_roles = {"admin"}

class IsManagerOrAdmin(HasRole):
    required_roles = {"manager", "admin"}