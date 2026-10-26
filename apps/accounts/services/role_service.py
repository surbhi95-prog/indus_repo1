# from django.db import transaction

# from apps.accounts.models.role import Role


# class RoleService:
#     """
#     Service layer for Role operations.
#     """

#     @staticmethod
#     @transaction.atomic
#     def create_role(validated_data):
#         """
#         Create a new role.
#         """
#         return Role.objects.create(
#             **validated_data
#         )

#     @staticmethod
#     def get_roles():
#         """
#         Get all active roles.
#         """
#         return (
#             Role.objects.select_related(
#                 "company",
#                 "plant",
#                 "department"
#             )
#             .filter(is_active=True)
#             .order_by("name")
#         )

#     @staticmethod
#     def get_role(role_id):
#         """
#         Get role by id.
#         """
#         return Role.objects.select_related(
#             "company",
#             "plant",
#             "department"
#         ).get(
#             id=role_id
#         )

#     @staticmethod
#     @transaction.atomic
#     def update_role(role, validated_data):
#         """
#         Update role.
#         """
#         for field, value in validated_data.items():
#             setattr(role, field, value)

#         role.save()

#         return role

#     @staticmethod
#     @transaction.atomic
#     def delete_role(role):
#         """
#         Delete role.
#         """
#         role.delete()



from django.db import transaction

from rest_framework.exceptions import ValidationError

from apps.accounts.models.role import Role


class RoleService:

    @staticmethod
    @transaction.atomic
    def create_role(validated_data):
        validated_data["department"] = None
        
        return Role.objects.create(
            **validated_data
        )

    @staticmethod
    def get_roles(
        company_id=None,
        plant_id=None
    ):

        queryset = (
            Role.objects
            .select_related(
                "company",
                "plant",
                "department"
            )
            .filter(
                is_active=True
            )
        )

        # -----------------------------------------------------
        # COMPANY FILTER
        # -----------------------------------------------------

        if company_id:

            queryset = queryset.filter(
                company_id=company_id
            )

        # -----------------------------------------------------
        # PLANT FILTER
        # -----------------------------------------------------

        if plant_id:

            queryset = queryset.filter(
                plant_id=plant_id
            )

        return queryset.order_by(
            "scope",
            "name"
        )

    @staticmethod
    def get_role(role_id):

        return (
            Role.objects
            .select_related(
                "company",
                "plant",
                "department"
            )
            .get(
                id=role_id
            )
        )

    @staticmethod
    @transaction.atomic
    def update_role(role, validated_data):

        for field, value in validated_data.items():
            setattr(
                role,
                field,
                value
            )

        role.save()

        return role

    @staticmethod
    @transaction.atomic
    def delete_role(role):

        role.delete()   