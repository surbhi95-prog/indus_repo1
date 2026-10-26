# # from django.db import transaction
# # from django.db.models import Q
# # from rest_framework.exceptions import ValidationError

# # from apps.accounts.models.permission import Permission
# # from apps.accounts.models import UserRole, user

# # class PermissionService:

# #     @staticmethod
# #     @transaction.atomic
# #     def create_permission(validated_data):

# #         permission = Permission.objects.create(

# #             company=validated_data["company"],

# #             plant=validated_data.get("plant"),

# #             department=validated_data.get("department"),

# #             scope=validated_data["scope"],

# #             module=validated_data["module"],

# #             action=validated_data["action"],

# #             code=validated_data["code"],

# #             description=validated_data.get("description"),

# #         )

# #         return permission

# #     @staticmethod
# #     def get_permissions_for_user(user):

# #       is_super_admin = UserRole.objects.filter(
# #         user=user,
# #         role__code="SUPER_ADMIN"
# #     ).exists()

# #       if is_super_admin:

# #        return Permission.objects.select_related(
# #             "company",
# #             "plant",
# #             "department"
# #         ).order_by(
# #             "module",
# #             "action"
# #         )

# #       queryset = Permission.objects.select_related(
# #             "company",
# #             "plant",
# #             "department"
# #         ).filter(
# #             company=user.company
# #         )

# #       if user.department:
# #             queryset = queryset.filter(
# #                 Q(scope="company") |
# #                 Q(scope="plant", plant=user.plant) |
# #                 Q(
# #                     scope="department",
# #                     plant=user.plant,
# #                     department=user.department
# #                 )
# #             )
# #       elif user.plant:
# #             queryset = queryset.filter(
# #                 Q(scope="company") |
# #                 Q(scope="plant", plant=user.plant) |
# #                 Q(scope="department", plant=user.plant)
# #             )

# #       return queryset.order_by(
# #             "module",
# #             "action"
# #         )




# from django.db import transaction
# from django.db.models import Q

# from rest_framework.exceptions import ValidationError

# from apps.accounts.models.permission import Permission


# class PermissionService:

#     @staticmethod
#     @transaction.atomic
#     def create_permission(validated_data):

#         module = validated_data["module"].strip().lower()

#         action = validated_data["action"].strip().lower()

#         code = validated_data.get("code")

#         if code:

#             code = code.strip().lower()

#         else:

#             code = f"{module}.{action}"

#         duplicate = Permission.objects.filter(
#             company=validated_data["company"],
#             plant=validated_data.get("plant"),
#             department=validated_data.get("department"),
#             module=module,
#             action=action,
#         ).exists()

#         if duplicate:

#             raise ValidationError({
#                 "permission":
#                 "Permission already exists for this scope."
#             })

#         permission = Permission.objects.create(

#             company=validated_data["company"],

#             plant=validated_data.get("plant"),

#             department=validated_data.get("department"),

#             scope=validated_data["scope"],

#             module=module,

#             action=action,

#             code=code,

#             description=validated_data.get("description"),

#         )

#         return permission

#     @staticmethod
#     def get_permissions_for_user(user):

#         # --------------------------------------------------
#         # Super Admin
#         # --------------------------------------------------

#         if user.is_superuser:

#             return Permission.objects.select_related(
#                 "company",
#                 "plant",
#                 "department"
#             ).all().order_by(
#                 "module",
#                 "action"
#             )

#         # --------------------------------------------------
#         # User must belong to a company
#         # --------------------------------------------------

#         if not user.company:

#             return Permission.objects.none()

#         queryset = Permission.objects.select_related(
#             "company",
#             "plant",
#             "department"
#         ).filter(
#             company=user.company
#         )

#         # --------------------------------------------------
#         # Department User
#         # --------------------------------------------------

#         if user.department:

#             return queryset.filter(

#                 Q(
#                     scope="company"
#                 )

#                 |

#                 Q(
#                     scope="plant",
#                     plant=user.plant
#                 )

#                 |

#                 Q(
#                     scope="department",
#                     plant=user.plant,
#                     department=user.department
#                 )

#             ).order_by(
#                 "module",
#                 "action"
#             )

#         # --------------------------------------------------
#         # Plant User
#         # --------------------------------------------------

#         if user.plant:

#             return queryset.filter(

#                 Q(
#                     scope="company"
#                 )

#                 |

#                 Q(
#                     scope="plant",
#                     plant=user.plant
#                 )

#                 |

#                 Q(
#                     scope="department",
#                     plant=user.plant
#                 )

#             ).order_by(
#                 "module",
#                 "action"
#             )

#         # --------------------------------------------------
#         # Company User
#         # --------------------------------------------------

#         return queryset.filter(
#             scope="company"
#         ).order_by(
#             "module",
#             "action"
#         )


from django.db import transaction

from django.db.models import Q

from rest_framework.exceptions import ValidationError

# from apps.accounts.models import user
from apps.accounts.models.permission import Permission
from apps.masters.models.company import Company
from apps.masters.models.plant import Plant

class PermissionService:

    # =========================================================
    # CREATE PERMISSION
    # =========================================================

    @staticmethod
    @transaction.atomic
    def create_permission(validated_data):

        # -----------------------------------------------------
        # GET VALUES
        # -----------------------------------------------------

        company = validated_data["company"]
        plant = validated_data.get("plant")
        department = validated_data.get("department")

        # -----------------------------------------------------
        # NORMALIZE VALUES
        # -----------------------------------------------------

        module = validated_data["module"].strip().lower()
        tab = validated_data.get("tab")
        action = validated_data["action"].strip().lower()
        scope = validated_data["scope"].strip().lower()

        if tab:
            tab = tab.strip().lower()

        # -----------------------------------------------------
        # GENERATE CODE
        # -----------------------------------------------------

        if tab:
            code = f"{module}.{tab}.{action}"
        else:
            code = f"{module}.{action}"

        # -----------------------------------------------------
        # VALIDATE SCOPE
        # -----------------------------------------------------

        if scope != "company":

            raise ValidationError({
                "scope": (
                    "Invalid permission scope. "
                    "Only company scope is allowed."
            )
        })
            
        plant = None
        department = None

        # -----------------------------------------------------
        # COMPANY SCOPE
        # -----------------------------------------------------

        if scope == "company":

            plant = None
            department = None

        # -----------------------------------------------------
        # PLANT SCOPE
        # -----------------------------------------------------

        # elif scope == "plant":

        #     if not plant:
        #         raise ValidationError({
        #             "plant": (
        #                 "Plant is required "
        #                 "for plant scope."
        #             )
        #         })

        #     if plant.company_id != company.id:
        #         raise ValidationError({
        #             "plant": (
        #                 "Plant does not belong "
        #                 "to selected company."
        #             )
        #         })

        #     department = None

        # -----------------------------------------------------
        # DEPARTMENT SCOPE
        # -----------------------------------------------------

        # elif scope == "department":

        #     if not plant:
        #         raise ValidationError({
        #             "plant": (
        #                 "Plant is required "
        #                 "for department scope."
        #             )
        #         })

        #     if not department:
        #         raise ValidationError({
        #             "department": (
        #                 "Department is required "
        #                 "for department scope."
        #             )
        #         })

        #     if plant.company_id != company.id:
        #         raise ValidationError({
        #             "plant": (
        #                 "Plant does not belong "
        #                 "to selected company."
        #             )
        #         })

        #     if department.plant_id != plant.id:
        #         raise ValidationError({
        #             "department": (
        #                 "Department does not belong "
        #                 "to selected plant."
        #             )
        #         })

        # -----------------------------------------------------
        # DUPLICATE CHECK
        #
        # company
        # + scope
        # + plant
        # + department
        # + code
        # -----------------------------------------------------

        duplicate = Permission.objects.filter(
            company=company,
            plant=plant,
            department=department,
            scope=scope,
            code=code,
        ).exists()

        if duplicate:

            raise ValidationError({
                "permission": (
                    "Permission with this code "
                    "already exists for this scope."
                )
            })

        # -----------------------------------------------------
        # CREATE PERMISSION
        # -----------------------------------------------------

        permission = Permission.objects.create(
            company=company,
            plant=plant,
            department=department,
            scope=scope,
            module=module,
            tab=tab,
            action=action,
            code=code,
            description=validated_data.get(
                "description"
            ),
        )

        return permission

    # =========================================================
    # GET PERMISSIONS FOR USER
    # =========================================================

    # @staticmethod
    # def get_permissions_for_user(user):

    #     # -----------------------------------------------------
    #     # SUPERUSER
    #     # -----------------------------------------------------

    #     if user.is_superuser:

    #         return (
    #             Permission.objects
    #             .select_related(
    #                 "company",
    #                 "plant",
    #                 "department",
    #             )
    #             .all()
    #             .order_by(
    #                 "module",
    #                 "code",
    #             )
    #         )

    #     # -----------------------------------------------------
    #     # COMPANY REQUIRED
    #     # -----------------------------------------------------

    #     if not user.company:

    #         return Permission.objects.none()

    #     queryset = (
    #         Permission.objects
    #         .select_related(
    #             "company",
    #             "plant",
    #             "department",
    #         )
    #         .filter(
    #             company=user.company
    #         )
    #     )

    #     # -----------------------------------------------------
    #     # DEPARTMENT USER
    #     # -----------------------------------------------------

    #     if user.department:

    #         return queryset.filter(

    #             Q(
    #                 scope="company"
    #             )

    #             |

    #             Q(
    #                 scope="plant",
    #                 plant=user.plant,
    #             )

    #             |

    #             Q(
    #                 scope="department",
    #                 plant=user.plant,
    #                 department=user.department,
    #             )

    #         ).order_by(
    #             "module",
    #             "code",
    #         )

    #     # -----------------------------------------------------
    #     # PLANT USER
    #     # -----------------------------------------------------

    #     if user.plant:

    #         return queryset.filter(

    #             Q(
    #                 scope="company"
    #             )

    #             |

    #             Q(
    #                 scope="plant",
    #                 plant=user.plant,
    #             )

    #             |

    #             Q(
    #                 scope="department",
    #                 plant=user.plant,
    #             )

    #         ).order_by(
    #             "module",
    #             "code",
    #         )

    #     # -----------------------------------------------------
    #     # COMPANY USER
    #     # -----------------------------------------------------

    #     return queryset.filter(
    #         scope="company"
    #     ).order_by(
    #         "module",
    #         "code",
    #     )
    @staticmethod
    def get_permissions_for_user(
        user,
        company_id=None,
        plant_id=None,
    ):

        # =====================================================
        # PLANT FILTER DEPENDS ON COMPANY
        # =====================================================

        if plant_id and not company_id:

            raise ValidationError({
                "company_id":
                    "Company ID is required when plant ID is provided."
            })

        # =====================================================
        # VALIDATE COMPANY
        # =====================================================

        company = None

        if company_id:

            try:

                company = Company.objects.get(
                    id=company_id
                )

            except Company.DoesNotExist:

                raise ValidationError({
                    "company_id":
                        "Company not found."
                })

        # =====================================================
        # VALIDATE PLANT
        # =====================================================

        plant = None

        if plant_id:

            try:

                plant = Plant.objects.get(
                    id=plant_id,
                    company_id=company_id
                )

            except Plant.DoesNotExist:

                raise ValidationError({
                    "plant_id":
                        "Plant does not belong to the selected company."
                })

        # =====================================================
        # BASE QUERYSET
        # =====================================================
        #
        # IMPORTANT:
        # queryset is created BEFORE applying any filters.
        # This prevents:
        #
        # cannot access local variable 'queryset'
        #
        # =====================================================

        if user.is_superuser:

            queryset = (
                Permission.objects
                .select_related(
                    "company",
                    "plant",
                    "department",
                )
                .all()
            )

        else:

            # -------------------------------------------------
            # USER MUST HAVE COMPANY
            # -------------------------------------------------

            if not user.company:

                return Permission.objects.none()

            queryset = (
                Permission.objects
                .select_related(
                    "company",
                    "plant",
                    "department",
                )
                .filter(
                    company=user.company
                )
            )

        # =====================================================
        # COMPANY FILTER
        # =====================================================

        if company_id:

            queryset = queryset.filter(
                company_id=company_id
            )

        # =====================================================
        # PLANT FILTER
        # =====================================================

        if plant_id:

            queryset = queryset.filter(
                plant_id=plant_id
            )

        # =====================================================
        # DEPARTMENT USER
        # =====================================================

        if user.department:

            return queryset.filter(

                Q(
                    scope="company"
                )

                |

                Q(
                    scope="plant",
                    plant=user.plant,
                )

                |

                Q(
                    scope="department",
                    plant=user.plant,
                    department=user.department,
                )

            ).order_by(
                "module",
                "code",
            )

        # =====================================================
        # PLANT USER
        # =====================================================

        if user.plant:

            return queryset.filter(

                Q(
                    scope="company"
                )

                |

                Q(
                    scope="plant",
                    plant=user.plant,
                )

                |

                Q(
                    scope="department",
                    plant=user.plant,
                )

            ).order_by(
                "module",
                "code",
            )

        # =====================================================
        # COMPANY USER
        # =====================================================

        return queryset.filter(
            scope="company"
        ).order_by(
            "module",
            "code",
        )