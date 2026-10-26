
from rest_framework.permissions import BasePermission

from apps.accounts.models.user_role import UserRole
from apps.accounts.models.role_permission import RolePermission


class HasSalesOrderCreatePermission(BasePermission):

    message = "You do not have permission to create Sales Orders."

    required_permission_code = "sales.sales_order.create"

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        # Get roles assigned to the current user.
        assigned_roles = UserRole.objects.filter(
            user=request.user,
            role__is_active=True
        ).values_list("role_id", flat=True)

        # Check whether any assigned role grants this action.
        return RolePermission.objects.filter(
            role_id__in=assigned_roles,
            permission__code=self.required_permission_code
        ).exists()
