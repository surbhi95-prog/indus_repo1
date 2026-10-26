# from aiohttp.test_utils import Self
# from attr import attrs
# from django.contrib.auth import get_user_model

# from rest_framework import request, serializers

# from apps.accounts.models.user_role import UserRole
# from apps.hrms.models.employee import Employee
# from apps.accounts.models.role import Role
# from apps.hrms.services.user_service import UserService
# from apps.masters.models.company import Company
# from apps.masters.models.plant import Plant
# from apps.masters.models.department import Department
# from apps.accounts.services.password_encryption_service import (
#     PasswordEncryptionService
# )


# User = get_user_model()

# from uuid import UUID

# from django.db import transaction
# from rest_framework import serializers

# from apps.hrms.models.employee import Employee

# from apps.hrms.services.user_service import UserService


# class CreateUserSerializer(serializers.Serializer):

#     # employee_code = serializers.CharField(
#     #     max_length=50
#     # )

#     username = serializers.CharField(
#         max_length=100
#     )

#     first_name = serializers.CharField(
#         max_length=100
#     )

#     last_name = serializers.CharField(
#         max_length=100,
#         required=False,
#         allow_blank=True
#     )

#     password = serializers.CharField(
#         write_only=True,
#         min_length=8,
#         required=False,
#         allow_blank=True
#     )

#     # ---------------------------------------------------------
#     # COMPANY
#     # ---------------------------------------------------------

#     company = serializers.UUIDField(
#         required=True
#     )

#     # ---------------------------------------------------------
#     # PLANT
#     # Accept UUID OR ""
#     # ---------------------------------------------------------

#     plant = serializers.CharField(
#         required=False,
#         allow_blank=True,
#         allow_null=True
#     )

#     # ---------------------------------------------------------
#     # DEPARTMENT
#     # Accept UUID OR ""
#     # ---------------------------------------------------------

#     department = serializers.CharField(
#         required=False,
#         allow_blank=True,
#         allow_null=True
#     )
#         # ---------------------------------------------------------
#     # USER SCOPE
#     # ---------------------------------------------------------

#     scope = serializers.ChoiceField(
#         choices=[
#             ("company", "Company"),
#             ("plant", "Plant"),
#             ("department", "Department"),
#         ],
#         required=True
#     )
#     employment_type = serializers.CharField(
#         max_length=50
#     )

#     joining_date = serializers.DateField()

#     status = serializers.CharField(
#         max_length=30
#     )

#     email = serializers.EmailField(
#     required=False,
#     allow_blank=True,
#     allow_null=True
# )

#     phone = serializers.CharField(
#         max_length=20,
#         required=False,
#         allow_blank=True
#     )

#     role_ids = serializers.ListField(
#         child=serializers.UUIDField(),
#         required=True,
#         allow_empty=False
#     )

#     # =========================================================
#     # VALIDATE
#     # =========================================================

#     def validate(self, attrs):

#         request = self.context.get("request")

#         if not request:
#             raise serializers.ValidationError({
#                 "request":
#                     "Request context is required."
#             })

#         requesting_user = request.user

#         # =====================================================
#         # NORMALIZE PLANT
#         # =====================================================

#         plant = attrs.get("plant")

#         if plant in ("", None):
#             plant = None

#         else:
#             try:
#                 plant = UUID(str(plant))
#             except (ValueError, TypeError, AttributeError):

#                 raise serializers.ValidationError({
#                     "plant":
#                         "Invalid plant UUID."
#                 })

#         # =====================================================
#         # NORMALIZE DEPARTMENT
#         # =====================================================

#         department = attrs.get("department")

#         if department in ("", None):
#             department = None

#         else:
#             try:
#                 department = UUID(str(department))
#             except (ValueError, TypeError, AttributeError):

#                 raise serializers.ValidationError({
#                     "department":
#                         "Invalid department UUID."
#                 })

#         attrs["plant"] = plant
#         attrs["department"] = department
#         # =====================================================
# # CHECK USERNAME
# # =====================================================

#         if Employee.objects.filter(
#             username__iexact=attrs["username"]
#             ).exists():

#             raise serializers.ValidationError({
#                 "username":
#                 "Employee with this username already exists."
#          })

#         # =====================================================
#         # CHECK EMPLOYEE CODE
#         # =====================================================

#         if Employee.objects.filter(
#             employee_code=attrs["employee_code"]
#         ).exists():

#             raise serializers.ValidationError({
#                 "employee_code":
#                     "Employee with this employee code already exists."
#             })

#         # =====================================================
#         # CHECK EMAIL
#         # =====================================================

#         # =====================================================
# # CHECK EMAIL
# # =====================================================

#         email = attrs.get("email")

#         if email:
#             if Employee.objects.filter(
#             email__iexact=email
#         ).exists():

#                 raise serializers.ValidationError({
#                 "email":
#                 "Employee with this email already exists."
#             })

#             if User.objects.filter(
#                 email__iexact=email
#             ).exists():

#                 raise serializers.ValidationError({
#                 "email":
#                 "User with this email already exists."
#         })

#         # # =====================================================
#         # # CHECK SUPER ADMIN
#         # # =====================================================

#         # is_super_admin = UserService.is_super_admin(
#         #     requesting_user
#         # )

#         # # =====================================================
#         # # CHECK PLANT HR
#         # # =====================================================

#         # is_plant_hr = requesting_user.assigned_roles.filter(
#         #     role__code__in=[
#         #         "PLANT_HR",
#         #         "HR_MANAGER",
#         #     ],
#         #     role__scope="plant",
#         #     role__is_active=True
#         # ).exists()

#         # # =====================================================
#         # # AUTHORIZATION
#         # # =====================================================

#         # if not is_super_admin and not is_plant_hr:

#         #     raise serializers.ValidationError({
#         #         "permission":
#         #             "You are not allowed to create users."
#         #     })
#         # =====================================================
# # # CHECK SUPER ADMIN
# # # =====================================================

# #         is_super_admin = UserService.is_super_admin(
# #             requesting_user
# #         )

# # # =====================================================
# # # CHECK PLANT HR
# # # =====================================================

# #         is_plant_hr = requesting_user.assigned_roles.filter(
# #         role__code__in=[
# #             "PLANT_HR",
# #             "HR_MANAGER",
# #         ],
# #         role__scope="plant",
# #         role__is_active=True
# #     ).exists()

# # # =====================================================
# # # AUTHORIZATION
# # # =====================================================

# #         if not is_super_admin and not is_plant_hr:

# #             raise serializers.ValidationError({
# #             "permission":
# #             "You are not allowed to create users."
# #     })
#         # =====================================================
#         # PLANT HR RESTRICTION
#         # =====================================================

#         # if not is_super_admin:

#         #     # -------------------------------------------------
#         #     # COMPANY
#         #     # -------------------------------------------------

#         #     if (
#         #         not requesting_user.company_id
#         #         or
#         #         str(requesting_user.company_id)
#         #         != str(attrs["company"])
#         #     ):

#         #         raise serializers.ValidationError({
#         #             "company":
#         #                 "You can only create users "
#         #                 "within your company."
#         #         })

#         #     # -------------------------------------------------
#         #     # PLANT
#         #     # -------------------------------------------------

#         #     if not requesting_user.plant_id:

#         #         raise serializers.ValidationError({
#         #             "plant":
#         #                 "Your account is not assigned to a plant."
#         #         })

#         #     if not plant:

#         #         raise serializers.ValidationError({
#         #             "plant":
#         #                 "Plant is required for Plant HR "
#         #                 "user creation."
#         #         })

#         #     if (
#         #         str(requesting_user.plant_id)
#         #         != str(plant)
#         #     ):

#         #         raise serializers.ValidationError({
#         #             "plant":
#         #                 "You can only create users "
#         #                 "within your plant."
#         #         })

#         # =====================================================
#         # FETCH ROLES
#         # =====================================================

#         role_ids = attrs["role_ids"]

#         roles = list(
#             Role.objects
#             .filter(
#                 id__in=role_ids,
#                 is_active=True
#             )
#             .select_related(
#                 "company",
#                 "plant",
#                 "department"
#             )
#         )

#         # =====================================================
#         # VALIDATE ROLE COUNT
#         # =====================================================

#         if len(roles) != len(set(role_ids)):

#             raise serializers.ValidationError({
#                 "role_ids":
#                     "One or more roles are invalid."
#             })

#         # =====================================================
#         # DETERMINE REQUIRED SCOPE
#         # =====================================================

#         scopes = {
#             role.scope
#             for role in roles
#         }

#         # =====================================================
#         # COMPANY LEVEL ROLE
#         # =====================================================

#         if "company" in scopes:

#             if not attrs.get("company"):

#                 raise serializers.ValidationError({
#                     "company":
#                         "Company is required for "
#                         "company-level roles."
#                 })

#         # =====================================================
#         # PLANT LEVEL ROLE
#         # =====================================================

#         if "plant" in scopes:

#             if not plant:

#                 raise serializers.ValidationError({
#                     "plant":
#                         "Plant is required for "
#                         "plant-level roles."
#                 })

#         # =====================================================
#         # DEPARTMENT LEVEL ROLE
#         # =====================================================

#         # if "department" in scopes:

#         #     if not plant:

#         #         raise serializers.ValidationError({
#         #             "plant":
#         #                 "Plant is required for "
#         #                 "department-level roles."
#         #         })

#         #     if not department:

#         #         raise serializers.ValidationError({
#         #             "department":
#         #                 "Department is required for "
#         #                 "department-level roles."
#         #         })

#         # =====================================================
#         # VALIDATE EACH ROLE
#         # =====================================================

#         for role in roles:

#             # -------------------------------------------------
#             # COMPANY ROLE
#             # -------------------------------------------------

#             if role.scope == "company":

#                 if (
#                     str(role.company_id)
#                     != str(attrs["company"])
#                 ):

#                     raise serializers.ValidationError({
#                         "role_ids":
#                             f"Role '{role.name}' does not belong "
#                             "to employee's company."
#                     })

#             # -------------------------------------------------
#             # PLANT ROLE
#             # -------------------------------------------------

#             elif role.scope == "plant":

#                 if (
#                     str(role.company_id)
#                     != str(attrs["company"])
#                 ):

#                     raise serializers.ValidationError({
#                         "role_ids":
#                             f"Role '{role.name}' does not belong "
#                             "to employee's company."
#                     })

#                 if not plant:

#                     raise serializers.ValidationError({
#                         "plant":
#                             f"Plant is required for "
#                             f"role '{role.name}'."
#                     })

#                 if (
#                     str(role.plant_id)
#                     != str(plant)
#                 ):

#                     raise serializers.ValidationError({
#                         "role_ids":
#                             f"Role '{role.name}' does not belong "
#                             "to employee's plant."
#                     })

#             # # -------------------------------------------------
#             # # DEPARTMENT ROLE
#             # # -------------------------------------------------

#             # elif role.scope == "department":

#             #     if (
#             #         str(role.company_id)
#             #         != str(attrs["company"])
#             #     ):

#             #         raise serializers.ValidationError({
#             #             "role_ids":
#             #                 f"Role '{role.name}' does not belong "
#             #                 "to employee's company."
#             #         })

#             #     if not plant:

#             #         raise serializers.ValidationError({
#             #             "plant":
#             #                 f"Plant is required for "
#             #                 f"role '{role.name}'."
#             #         })

#             #     if (
#             #         str(role.plant_id)
#             #         != str(plant)
#             #     ):

#             #         raise serializers.ValidationError({
#             #             "role_ids":
#             #                 f"Role '{role.name}' does not belong "
#             #                 "to employee's plant."
#             #         })

#             #     if not department:

#             #         raise serializers.ValidationError({
#             #             "department":
#             #                 f"Department is required for "
#             #                 f"role '{role.name}'."
#             #         })

#             #     if (
#             #         str(role.department_id)
#             #         != str(department)
#             #     ):

#             #         raise serializers.ValidationError({
#             #             "role_ids":
#             #                 f"Role '{role.name}' does not belong "
#             #                 "to employee's department."
#             #         })

#         # # =====================================================
#         # # PLANT HR CAN ONLY ASSIGN DEPARTMENT ROLES
#         # # =====================================================

#         # if not is_super_admin:

#         #     for role in roles:

#         #         if role.scope != "department":

#         #             raise serializers.ValidationError({
#         #                 "role_ids": (
#         #                     f"Plant HR cannot assign "
#         #                     f"'{role.name}'. "
#         #                     "Only department-level roles "
#         #                     "can be assigned."
#         #                 )
#         #             })
#     #         # -------------------------------------------------
#     # # UNSUPPORTED ROLE SCOPE
#     # # -------------------------------------------------

#     #         else:

#     #             raise serializers.ValidationError({
#     #                 "role_ids": (
#     #                     f"Role '{role.name}' uses unsupported "
#     #                     f"scope '{role.scope}'. "
#     #                     "Only company and plant roles are "
#     #                     "allowed for user creation."
#     #                 )
#     #             })
#                 # =====================================================
#         # SAVE ROLES FOR SERVICE
#         # =====================================================

#         attrs["roles"] = roles

#         return attrs

#     # =========================================================
#     # CREATE USER
#     # =========================================================

#     @staticmethod
#     @transaction.atomic
#     def create_user(validated_data):

#         roles = validated_data.pop("roles")
#         password = validated_data.pop("password")

#         # -----------------------------------------------------
#         # Optional organization values
#         # -----------------------------------------------------

#         company_id = validated_data["company"]

#         plant_id = validated_data.get("plant")
#         department_id = validated_data.get("department")

#         # -----------------------------------------------------
#         # Create Employee
#         # -----------------------------------------------------

#         employee = Employee.objects.create(
#             employee_code=validated_data["employee_code"],

#             first_name=validated_data["first_name"],

#             last_name=validated_data.get(
#                 "last_name",
#                 ""
#             ),

#             company_id=company_id,

#             plant_id=plant_id,

#             department_id=department_id,

#             employment_type=validated_data[
#                 "employment_type"
#             ],

#             joining_date=validated_data[
#                 "joining_date"
#             ],

#             status=validated_data[
#                 "status"
#             ],

#             email=validated_data[
#                 "email"
#             ],

#             phone=validated_data.get(
#                 "phone",
#                 ""
#             ),
#         )

#         # -----------------------------------------------------
#         # Create User
#         # -----------------------------------------------------

#         user = User.objects.create_user(
#             email=employee.email,

#             password=password,

#             first_name=employee.first_name,

#             last_name=employee.last_name or "",

#             employee=employee,

#             company=employee.company,

#             plant=employee.plant,

#             department=employee.department,

#             scope=validated_data["scope"],

#             is_active=True,
#         )

#         # -----------------------------------------------------
#         # Assign Roles
#         # -----------------------------------------------------

#         user_roles = [
#             UserRole(
#                 user=user,
#                 role=role
#             )
#             for role in roles
#         ]

#         UserRole.objects.bulk_create(
#             user_roles
#         )

#         return user

# # =============================================================
# # USER SERIALIZER
# # =============================================================

# class UserSerializer(serializers.ModelSerializer):

#     employee_id = serializers.UUIDField(
#         source="employee.id",
#         read_only=True
#     )

#     employee_code = serializers.CharField(
#         source="employee.employee_code",
#         read_only=True
#     )

#     employee_name = serializers.SerializerMethodField()

#     company_id = serializers.UUIDField(
#         source="company.id",
#         read_only=True
#     )

#     plant_id = serializers.UUIDField(
#         source="plant.id",
#         read_only=True
#     )

#     department_id = serializers.UUIDField(
#         source="department.id",
#         read_only=True
#     )
#     scope = serializers.CharField(
#         read_only=True
#     )
#     roles = serializers.SerializerMethodField()

#     class Meta:

#         model = User

#         fields = [
#             "id",

#             "employee_id",
#             "employee_code",
#             "employee_name",

#             "email",

#             "company_id",
#             "plant_id",
#             "department_id",
#             "scope",
#             "is_active",

#             "roles",
#         ]

#     def get_employee_name(self, obj):

#         if not obj.employee:
#             return None

#         return (
#             f"{obj.employee.first_name} "
#             f"{obj.employee.last_name or ''}"
#         ).strip()

#     def get_roles(self, obj):

#         return [
#             {
#                 "id": str(item.role.id),
#                 "name": item.role.name,
#                 "code": item.role.code,
#                 "scope": item.role.scope,
#             }
#             for item in obj.assigned_roles.select_related(
#                 "role"
#             ).all()
#         ]

# # class UserListSerializer(serializers.ModelSerializer):

# #     company_id = serializers.SerializerMethodField()
# #     company_name = serializers.SerializerMethodField()

# #     plant_id = serializers.SerializerMethodField()
# #     plant_name = serializers.SerializerMethodField()

# #     department_id = serializers.SerializerMethodField()
# #     department_name = serializers.SerializerMethodField()

# #     roles = serializers.SerializerMethodField()

# #     class Meta:
# #         model = User

# #         fields = [
# #             "id",

# #             "email",
# #             "first_name",
# #             "last_name",

# #             "company_id",
# #             "company_name",

# #             "plant_id",
# #             "plant_name",

# #             "department_id",
# #             "department_name",

# #             "roles",

# #             "is_active",
# #             "is_staff",
# #             "is_superuser",
# #         ]

# #     def get_company_id(self, obj):

# #         return (
# #             str(obj.company.id)
# #             if obj.company
# #             else None
# #         )

# #     def get_company_name(self, obj):

# #         return (
# #             obj.company.name
# #             if obj.company
# #             else None
# #         )

# #     def get_plant_id(self, obj):

# #         return (
# #             str(obj.plant.id)
# #             if obj.plant
# #             else None
# #         )

# #     def get_plant_name(self, obj):

# #         return (
# #             obj.plant.name
# #             if obj.plant
# #             else None
# #         )

# #     def get_department_id(self, obj):

# #         return (
# #             str(obj.department.id)
# #             if obj.department
# #             else None
# #         )

# #     def get_department_name(self, obj):

# #         return (
# #             obj.department.name
# #             if obj.department
# #             else None
# #         )

# #     def get_roles(self, obj):

# #         return [
# #             {
# #                 "id": str(item.role.id),
# #                 "name": item.role.name,
# #                 "code": item.role.code,
# #                 "scope": item.role.scope,
# #             }
# #             for item in obj.assigned_roles.select_related(
# #                 "role"
# #             ).all()
# #         ]

# # =============================================================
# # USER UPDATE SERIALIZER
# # =============================================================

# class UserUpdateSerializer(serializers.Serializer):

#     # ---------------------------------------------------------
#     # USER FIELDS
#     # ---------------------------------------------------------

#     email = serializers.EmailField(
#         required=False,
#         allow_blank=True,
#         allow_null=True
#     )

#     first_name = serializers.CharField(
#         max_length=100,
#         required=False
#     )

#     last_name = serializers.CharField(
#         max_length=100,
#         required=False,
#         allow_blank=True
#     )

#     is_active = serializers.BooleanField(
#         required=False
#     )

#     # ---------------------------------------------------------
#     # EMPLOYEE FIELDS
#     # ---------------------------------------------------------

#     employee_code = serializers.CharField(
#         max_length=50,
#         required=False
#     )

#     phone = serializers.CharField(
#         max_length=20,
#         required=False,
#         allow_blank=True,
#         allow_null=True
#     )

#     employment_type = serializers.CharField(
#         max_length=50,
#         required=False
#     )

#     joining_date = serializers.DateField(
#         required=False,
#         allow_null=True
#     )

#     status = serializers.CharField(
#         max_length=30,
#         required=False
#     )

#     # ---------------------------------------------------------
#     # ORGANIZATION
#     # ---------------------------------------------------------

#     company = serializers.UUIDField(
#         required=False,
#         allow_null=True
#     )

#     plant = serializers.UUIDField(
#         required=False,
#         allow_null=True
#     )

#     department = serializers.UUIDField(
#         required=False,
#         allow_null=True
#     )
#     scope = serializers.ChoiceField(
#         choices=[
#             ("company", "Company"),
#             ("plant", "Plant"),
#             ("department", "Department"),
#         ],
#         required=False
#     )
#     # ---------------------------------------------------------
#     # ROLES
#     # ---------------------------------------------------------

#     role_ids = serializers.ListField(
#         child=serializers.UUIDField(),
#         required=False,
#         allow_empty=True
#     )

#     # =========================================================
#     # VALIDATE
#     # =========================================================

#     def validate(self, attrs):

#         user = self.instance

#         employee = user.employee

#         # -----------------------------------------------------
#         # EMAIL
#         # -----------------------------------------------------

#         if "email" in attrs:

#             email = attrs["email"]

#             if email:

#                 if User.objects.filter(
#                     email__iexact=email
#                 ).exclude(
#                     id=user.id
#                 ).exists():

#                     raise serializers.ValidationError({
#                         "email":
#                             "User with this email already exists."
#                     })

#                 if Employee.objects.filter(
#                     email__iexact=email
#                 ).exclude(
#                     id=employee.id if employee else None
#                 ).exists():

#                     raise serializers.ValidationError({
#                         "email":
#                             "Employee with this email already exists."
#                     })

#         # -----------------------------------------------------
#         # EMPLOYEE CODE
#         # -----------------------------------------------------

#         if employee and "employee_code" in attrs:

#             employee_code = attrs["employee_code"]

#             if Employee.objects.filter(
#                 employee_code=employee_code
#             ).exclude(
#                 id=employee.id
#             ).exists():

#                 raise serializers.ValidationError({
#                     "employee_code":
#                         "Employee with this employee code already exists."
#                 })

#         # -----------------------------------------------------
#         # ORGANIZATION
#         # -----------------------------------------------------

#         company_id = attrs.get(
#             "company",
#             user.company_id
#         )

#         plant_id = attrs.get(
#             "plant",
#             user.plant_id
#         )

#         department_id = attrs.get(
#             "department",
#             user.department_id
#         )

#         # -----------------------------------------------------
#         # COMPANY
#         # -----------------------------------------------------

#         company = None

#         if company_id:

#             try:
#                 company = Company.objects.get(
#                     id=company_id
#                 )

#             except Company.DoesNotExist:

#                 raise serializers.ValidationError({
#                     "company":
#                         "Company not found."
#                 })

#         # -----------------------------------------------------
#         # PLANT
#         # -----------------------------------------------------

#         plant = None

#         if plant_id:

#             try:
#                 plant = Plant.objects.get(
#                     id=plant_id,
#                     company=company
#                 )

#             except Plant.DoesNotExist:

#                 raise serializers.ValidationError({
#                     "plant":
#                         "Plant does not belong to selected company."
#                 })

#         # -----------------------------------------------------
#         # DEPARTMENT
#         # -----------------------------------------------------

#         department = None

#         if department_id:

#             try:
#                 department = Department.objects.get(
#                     id=department_id,
#                     plant=plant
#                 )

#             except Department.DoesNotExist:

#                 raise serializers.ValidationError({
#                     "department":
#                         "Department does not belong to selected plant."
#                 })

#         attrs["company"] = company
#         attrs["plant"] = plant
#         attrs["department"] = department

#         # -----------------------------------------------------
#         # ROLE VALIDATION
#         # -----------------------------------------------------

#         if "role_ids" in attrs:

#             role_ids = attrs["role_ids"]

#             roles = list(
#                 Role.objects.filter(
#                     id__in=role_ids,
#                     is_active=True
#                 )
#             )

#             if len(roles) != len(set(role_ids)):

#                 raise serializers.ValidationError({
#                     "role_ids":
#                         "One or more roles are invalid."
#                 })
            
#             # =====================================================
# # DEPARTMENT SCOPE DISABLED
# # =====================================================

#             department_roles = [
#                 role.name
#                 for role in roles
#                 if role.scope == "department"
#         ]

#             if department_roles:

#                 raise serializers.ValidationError({
#                     "role_ids": (
#                     "Department-level roles are not allowed "
#                     "for user creation."
#             )
#         })

#             for role in roles:

#                 if role.scope == "company":

#                     if (
#                         role.company_id != company.id
#                         if company
#                         else True
#                     ):

#                         raise serializers.ValidationError({
#                             "role_ids":
#                                 f"Role '{role.name}' "
#                                 "does not belong to selected company."
#                         })

#                 elif role.scope == "plant":

#                     if not plant:

#                         raise serializers.ValidationError({
#                             "plant":
#                                 f"Plant is required for role "
#                                 f"'{role.name}'."
#                         })

#                     if (
#                         role.company_id != company.id
#                         or role.plant_id != plant.id
#                     ):

#                         raise serializers.ValidationError({
#                             "role_ids":
#                                 f"Role '{role.name}' "
#                                 "does not belong to selected plant."
#                         })

#                 elif role.scope == "department":

#                     if not department:

#                         raise serializers.ValidationError({
#                             "department":
#                                 f"Department is required for role "
#                                 f"'{role.name}'."
#                         })

#                     if (
#                         role.company_id != company.id
#                         or role.plant_id != plant.id
#                         or role.department_id != department.id
#                     ):

#                         raise serializers.ValidationError({
#                             "role_ids":
#                                 f"Role '{role.name}' "
#                                 "does not belong to selected department."
#                         })

#             attrs["roles"] = roles

#         return attrs

# class UserListSerializer(serializers.ModelSerializer):

#     # =====================================================
#     # COMPANY
#     # =====================================================

#     company_id = serializers.UUIDField(
#         source="company.id",
#         read_only=True,
#         allow_null=True,
#     )

#     company_name = serializers.CharField(
#         source="company.name",
#         read_only=True,
#         allow_null=True,
#     )
#     scope = serializers.CharField(
#         read_only=True
#     )
#     # =====================================================
#     # PLANT
#     # =====================================================

#     plant_id = serializers.UUIDField(
#         source="plant.id",
#         read_only=True,
#         allow_null=True,
#     )

#     plant_name = serializers.CharField(
#         source="plant.name",
#         read_only=True,
#         allow_null=True,
#     )

#     # =====================================================
#     # DEPARTMENT
#     # =====================================================

#     department_id = serializers.UUIDField(
#         source="department.id",
#         read_only=True,
#         allow_null=True,
#     )

#     department_name = serializers.CharField(
#         source="department.name",
#         read_only=True,
#         allow_null=True,
#     )

#     # =====================================================
#     # EMPLOYEE
#     # =====================================================

#     employee_id = serializers.UUIDField(
#         source="employee.id",
#         read_only=True,
#         allow_null=True,
#     )

#     employee_code = serializers.CharField(
#         source="employee.employee_code",
#         read_only=True,
#         allow_null=True,
#     )

#     employee_name = serializers.SerializerMethodField()

#     # =====================================================
#     # ROLES
#     # =====================================================

#     roles = serializers.SerializerMethodField()

#     # =====================================================
#     # FULL NAME
#     # =====================================================

#     full_name = serializers.SerializerMethodField()

#     # =====================================================
#     # META
#     # =====================================================
#     password_recovery = serializers.SerializerMethodField()
#     class Meta:

#         model = User

#         fields = [
#             # ---------------------------------------------
#             # USER
#             # ---------------------------------------------

#             "id",
#             "email",
#             "first_name",
#             "last_name",
#             "full_name",

#             # ---------------------------------------------
#             # EMPLOYEE
#             # ---------------------------------------------

#             "employee_id",
#             "employee_code",
#             "employee_name",

#             # ---------------------------------------------
#             # COMPANY
#             # ---------------------------------------------

#             "company_id",
#             "company_name",

#             # ---------------------------------------------
#             # PLANT
#             # ---------------------------------------------

#             "plant_id",
#             "plant_name",

#             # ---------------------------------------------
#             # DEPARTMENT
#             # ---------------------------------------------

#             "department_id",
#             "department_name",
#             "scope",
#             # ---------------------------------------------
#             # ROLES
#             # ---------------------------------------------

#             "roles",
#             "password_recovery",

#             # ---------------------------------------------
#             # STATUS
#             # ---------------------------------------------

#             "is_active",
#             "is_staff",
#             "is_superuser",
#         ]

#     # =====================================================
#     # FULL NAME
#     # =====================================================

#     def get_full_name(self, obj):

#         name = f"{obj.first_name or ''} {obj.last_name or ''}"

#         return name.strip()

#     # =====================================================
#     # EMPLOYEE NAME
#     # =====================================================

#     def get_employee_name(self, obj):

#         if not obj.employee:
#             return None

#         name = (
#             f"{obj.employee.first_name or ''} "
#             f"{obj.employee.last_name or ''}"
#         )

#         return name.strip()

#     # =====================================================
#     # ROLES
#     # =====================================================

#     def get_roles(self, obj):

#         roles = []

#         for user_role in obj.assigned_roles.all():

#             role = user_role.role

#             if not role:
#                 continue

#             roles.append({
#                 "id": str(role.id),
#                 "name": role.name,
#                 "code": role.code,
#                 "scope": getattr(
#                     role,
#                     "scope",
#                     None
#                 ),
#                 "is_active": getattr(
#                     role,
#                     "is_active",
#                     True
#                 ),
#             })

#         return roles
    
#             # =====================================================
#     # PASSWORD RECOVERY
#     # =====================================================

#     def get_password_recovery(self, obj):

#         if not obj.encrypted_password:
#             return None

#         try:

#             return PasswordEncryptionService.decrypt(
#                 obj.encrypted_password
#             )

#         except Exception:

#             return None
from uuid import UUID

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db import transaction
from rest_framework import serializers

from apps.accounts.models.role import Role
from apps.accounts.models.user_role import UserRole
from apps.accounts.models.role_permission import RolePermission
from apps.accounts.services.password_encryption_service import (
    PasswordEncryptionService
)
from apps.hrms.models.shift import Shift
from apps.hrms.shift_types import normalize_shift_type
from apps.hrms.models.employee_shift import EmployeeShift
from apps.hrms.models.employee import Employee
from apps.masters.models.company import Company
from apps.masters.models.plant import Plant
from apps.masters.models.department import Department

# These models are created in the employee CRUD changes.
from apps.hrms.models.employee_profile import EmployeeProfile
from apps.hrms.models.employee_statutory import EmployeeStatutory
from apps.hrms.models.emergency_contact import EmployeeEmergencyContact
from apps.hrms.models.employee_document import EmployeeDocument

from apps.hrms.services.employee_code_service import generate_employee_code


User = get_user_model()


def _optional_uuid(value, field_name):
    """Convert empty/None to None and validate UUID values."""
    if value in ("", None):
        return None

    try:
        return UUID(str(value))
    except (ValueError, TypeError, AttributeError):
        raise serializers.ValidationError(
            {field_name: f"Invalid {field_name} UUID."}
        )
def _validate_user_shift(
    shift_id,
    company,
    plant,
    shift_name=None,
    shift_type=None,
    shift_start_time=None,
    shift_end_time=None,
):
    """
    Validate that the selected shift belongs to the
    same company and plant as the user.

    Also validates optional shift details supplied
    by frontend against the actual Shift master.
    """

    if not shift_id:
        raise serializers.ValidationError({
            "shift_id": "Shift is required."
        })

    if not plant:
        raise serializers.ValidationError({
            "plant": "Plant is required when assigning a shift."
        })

    try:
        shift = (
            Shift.objects
            .select_related("company", "plant")
            .get(
                id=shift_id,
                is_active=True,
                is_deleted=False,
            )
        )
    except Shift.DoesNotExist:
        raise serializers.ValidationError({
            "shift_id": "Selected shift does not exist or is inactive."
        })

    # -------------------------------------------------
    # COMPANY CHECK
    # -------------------------------------------------

    if shift.company_id != company.id:
        raise serializers.ValidationError({
            "shift_id":
                "Selected shift does not belong to the user's company."
        })

    # -------------------------------------------------
    # PLANT CHECK
    # -------------------------------------------------

    if shift.plant_id != plant.id:
        raise serializers.ValidationError({
            "shift_id":
                "Selected shift does not belong to the user's plant."
        })

    # -------------------------------------------------
    # SHIFT NAME CHECK
    # -------------------------------------------------

    if shift_name is not None:
        if shift.name.strip().lower() != shift_name.strip().lower():
            raise serializers.ValidationError({
                "shift_name":
                    "Shift name does not match the selected shift."
            })

    # -------------------------------------------------
    # SHIFT TYPE CHECK
    # -------------------------------------------------

    if shift_type is not None:
        if shift.shift_type != normalize_shift_type(shift_type):
            raise serializers.ValidationError({
                "shift_type":
                    "Shift type does not match the selected shift."
            })

    # -------------------------------------------------
    # SHIFT START TIME CHECK
    # -------------------------------------------------

    if shift_start_time is not None:
        if shift.start_time != shift_start_time:
            raise serializers.ValidationError({
                "shift_start_time":
                    "Shift start time does not match the selected shift."
            })

    # -------------------------------------------------
    # SHIFT END TIME CHECK
    # -------------------------------------------------

    if shift_end_time is not None:
        if shift.end_time != shift_end_time:
            raise serializers.ValidationError({
                "shift_end_time":
                    "Shift end time does not match the selected shift."
            })

    return shift

class CreateUserSerializer(serializers.Serializer):
    """
    Complete employee/user creation serializer.

    Employee code is NOT accepted from the frontend.
    It is generated by the backend.

    User permissions are intentionally NOT handled here.
    Role assignment is retained because it belongs to user creation.
    """

    # =========================================================
    # USER / EMPLOYEE BASIC DETAILS
    # =========================================================

    username = serializers.CharField(max_length=100)

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        required=True,
    )

    first_name = serializers.CharField(max_length=100)

    middle_name = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
    )

    last_name = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
    )

    email = serializers.EmailField(
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    phone = serializers.CharField(
        max_length=20,
        required=True,
    )

    # =========================================================
    # PERSONAL / PROFILE DETAILS
    # =========================================================

    marital_status = serializers.CharField(
        max_length=50,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    partner_name = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    current_address = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    permanent_address = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    dob = serializers.DateField(
        required=False,
        allow_null=True,
    )

    blood_group = serializers.CharField(
        max_length=10,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    doctor_name = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    doctor_address = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    doctor_phone_no = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    health_issues = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    # =========================================================
    # EMERGENCY CONTACT
    # =========================================================

    emergency_contact_name = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    emergency_contact_no = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    # =========================================================
    # EMPLOYMENT
    # =========================================================

    joining_date = serializers.DateField()

    employment_type = serializers.ChoiceField(
        choices=Employee.EMPLOYMENT_TYPE_CHOICES,
        required=True,
    )

    grade = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    designation = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    location = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    qualification = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    experience = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        required=False,
        allow_null=True,
    )

    employer_name = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    employer_address = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    # =========================================================
    # STATUTORY DETAILS
    # All are strings/text values.
    # =========================================================

    ppf_account_no = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    uan_no = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    esic_no = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    punching_code = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    aadhaar_no = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    pan_no = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    # =========================================================
    # ORGANIZATION
    # =========================================================

    company = serializers.UUIDField(required=True)

    plant = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    department = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    scope = serializers.ChoiceField(
        choices=("company", "plant", "department"),
        required=False,
        default="plant",
    )

    is_active = serializers.BooleanField(default=True)

    # =========================================================
    # SHIFT
    # =========================================================

    shift_id = serializers.UUIDField(
        required=True,
    )

    shift_name = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    shift_type = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    shift_start_time = serializers.TimeField(
        required=False,
        allow_null=True,
    )

    shift_end_time = serializers.TimeField(
        required=False,
        allow_null=True,
    )

    # =========================================================
    # ROLES
    # =========================================================

    role_ids = serializers.ListField(
        child=serializers.UUIDField(),
        required=True,
        allow_empty=False,
    )

    # =========================================================
    # DOCUMENTS
    #
    # The API may send:
    # documents = [file1, file2, ...]
    #
    # Keep this as write_only because files are stored through
    # EmployeeDocument and are returned separately.
    # =========================================================

    documents = serializers.ListField(
        child=serializers.FileField(),
        required=False,
        allow_empty=True,
        write_only=True,
    )

    # =========================================================
    # VALIDATION
    # =========================================================

    def validate(self, attrs):
        request = self.context.get("request")
        if request is None:
            raise serializers.ValidationError(
                {"request": "Request context is required."}
            )

        # -----------------------------------------------------
        # NORMALIZE ORGANIZATION UUIDS
        # -----------------------------------------------------

        plant_id = _optional_uuid(attrs.get("plant"), "plant")
        department_id = _optional_uuid(
            attrs.get("department"),
            "department",
        )

        attrs["plant"] = plant_id
        attrs["department"] = department_id

        company_id = attrs["company"]

        # -----------------------------------------------------
        # COMPANY
        # -----------------------------------------------------

        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            raise serializers.ValidationError(
                {"company": "Company not found."}
            )

        # -----------------------------------------------------
        # PLANT
        # Plant must belong to selected company.
        # -----------------------------------------------------

        plant = None

        if plant_id:
            try:
                plant = Plant.objects.get(
                    id=plant_id,
                    company=company,
                )
            except Plant.DoesNotExist:
                raise serializers.ValidationError(
                    {
                        "plant":
                            "Plant does not belong to selected company."
                    }
                )

        # -----------------------------------------------------
        # DEPARTMENT
        # Department cannot be supplied without plant.
        # -----------------------------------------------------

        department = None

        if department_id:
            if not plant:
                raise serializers.ValidationError(
                    {
                        "department":
                            "Plant is required when department is selected."
                    }
                )

            try:
                department = Department.objects.get(
                    id=department_id,
                    plant=plant,
                )
            except Department.DoesNotExist:
                raise serializers.ValidationError(
                    {
                        "department":
                            "Department does not belong to selected plant."
                    }
                )

        attrs["company"] = company
        attrs["plant"] = plant
        attrs["department"] = department
        # -----------------------------------------------------
# SHIFT VALIDATION
# -----------------------------------------------------

        shift = _validate_user_shift(
            shift_id=attrs.get("shift_id"),
            company=company,
            plant=plant,
            shift_name=attrs.get("shift_name"),
            shift_type=attrs.get("shift_type"),
            shift_start_time=attrs.get("shift_start_time"),
            shift_end_time=attrs.get("shift_end_time"),
        )

        attrs["shift"] = shift
        # -----------------------------------------------------
        # USERNAME
        # -----------------------------------------------------

        username = attrs["username"].strip()

        if not username:
            raise serializers.ValidationError(
                {"username": "Username cannot be empty."}
            )

        if Employee.objects.filter(
            username__iexact=username
        ).exists():
            raise serializers.ValidationError(
                {
                    "username":
                        "Employee with this username already exists."
                }
            )

        # if User.objects.filter(
        #     username__iexact=username
        # ).exists():
        #     raise serializers.ValidationError(
        #         {
        #             "username":
        #                 "User with this username already exists."
        #         }
        #     )

        attrs["username"] = username

        # -----------------------------------------------------
        # EMAIL
        # -----------------------------------------------------

        email = attrs.get("email")

        if email:
            email = email.strip().lower()
            attrs["email"] = email

            if Employee.objects.filter(
                email__iexact=email
            ).exists():
                raise serializers.ValidationError(
                    {
                        "email":
                            "Employee with this email already exists."
                    }
                )

            if User.objects.filter(
                email__iexact=email
            ).exists():
                raise serializers.ValidationError(
                    {
                        "email":
                            "User with this email already exists."
                    }
                )
        # -----------------------------------------------------
        # PHONE NUMBER VALIDATION
        # User phone, emergency contact phone and doctor phone
        # must all be different.
        # -----------------------------------------------------

        phone = (attrs.get("phone") or "").strip()
        emergency_phone = (
            attrs.get("emergency_contact_no") or ""
        ).strip()
        doctor_phone = (
            attrs.get("doctor_phone_no") or ""
        ).strip()

        # Save cleaned values back into attrs
        attrs["phone"] = phone
        attrs["emergency_contact_no"] = emergency_phone
        attrs["doctor_phone_no"] = doctor_phone

        if (
            phone
            and emergency_phone
            and phone == emergency_phone
        ):
            raise serializers.ValidationError(
                {
                    "emergency_contact_no":
                        "Emergency contact number must be different "
                        "from user phone number."
                }
            )

        if (
            phone
            and doctor_phone
            and phone == doctor_phone
        ):
            raise serializers.ValidationError(
                {
                    "doctor_phone_no":
                        "Doctor phone number must be different "
                        "from user phone number."
                }
            )

        if (
            emergency_phone
            and doctor_phone
            and emergency_phone == doctor_phone
        ):
            raise serializers.ValidationError(
                {
                    "doctor_phone_no":
                        "Doctor phone number must be different "
                        "from emergency contact number."
                }
            )
                # -----------------------------------------------------
        # SCOPE
        # -----------------------------------------------------

        scope = attrs.get("scope") or "plant"

        if scope == "plant" and not plant:
            raise serializers.ValidationError(
                {
                    "plant":
                        "Plant is required when scope is plant."
                }
            )

        if scope == "department":
            if not plant:
                raise serializers.ValidationError(
                    {
                        "plant":
                            "Plant is required when scope is department."
                    }
                )

            if not department:
                raise serializers.ValidationError(
                    {
                        "department":
                            "Department is required when scope is department."
                    }
                )

        attrs["scope"] = scope

        # -----------------------------------------------------
        # ROLE VALIDATION
        #
        # This is role assignment only.
        # No permission service / permission override logic is used.
        # -----------------------------------------------------

        role_ids = attrs["role_ids"]

        roles = list(
            Role.objects.filter(
                id__in=role_ids,
                is_active=True,
            ).select_related(
                "company",
                "plant",
                "department",
            )
        )

        if len(roles) != len(set(role_ids)):
            raise serializers.ValidationError(
                {
                    "role_ids":
                        "One or more roles are invalid."
                }
            )

        for role in roles:

            if role.scope == "company":

                if not company or role.company_id != company.id:
                    raise serializers.ValidationError(
                        {
                            "role_ids":
                                f"Role '{role.name}' does not belong "
                                "to selected company."
                        }
                    )

            elif role.scope == "plant":

                if not plant:
                    raise serializers.ValidationError(
                        {
                            "plant":
                                f"Plant is required for role "
                                f"'{role.name}'."
                        }
                    )

                if (
                    role.company_id != company.id
                    or role.plant_id != plant.id
                ):
                    raise serializers.ValidationError(
                        {
                            "role_ids":
                                f"Role '{role.name}' does not belong "
                                "to selected plant."
                        }
                    )

            elif role.scope == "department":

                if not department:
                    raise serializers.ValidationError(
                        {
                            "department":
                                f"Department is required for role "
                                f"'{role.name}'."
                        }
                    )

                if (
                    role.company_id != company.id
                    or role.plant_id != plant.id
                    or role.department_id != department.id
                ):
                    raise serializers.ValidationError(
                        {
                            "role_ids":
                                f"Role '{role.name}' does not belong "
                                "to selected department."
                        }
                    )

            else:
                raise serializers.ValidationError(
                    {
                        "role_ids":
                            f"Role '{role.name}' has unsupported scope "
                            f"'{role.scope}'."
                    }
                )

        attrs["roles"] = roles
        # -----------------------------------------------------
# DOCUMENT LIMIT
# -----------------------------------------------------

        documents = attrs.get("documents", [])

        if len(documents) > 4:
            raise serializers.ValidationError({
                "documents":
                    "Maximum 4 documents can be uploaded for a user."
            })
        return attrs

    # =========================================================
    # CREATE
    # =========================================================

    @staticmethod
    @transaction.atomic
    def create_user(validated_data):
        """
        Creates:
            1. Employee
            2. EmployeeProfile
            3. EmployeeStatutory
            4. Emergency Contact
            5. User
            6. UserRole records
            7. EmployeeDocument records

        Employee code is generated by backend.
        Password is stored using Django's normal password hashing.
        """

        request = validated_data.pop("_request", None)

        roles = validated_data.pop("roles", [])
        role_ids = validated_data.pop("role_ids", None)

        password = validated_data.pop("password")

        documents = validated_data.pop("documents", [])

        company = validated_data.pop("company")
        plant = validated_data.pop("plant", None)
        department = validated_data.pop("department", None)

        # -----------------------------------------------------
        # BACKEND EMPLOYEE CODE
        # -----------------------------------------------------

        employee_code = generate_employee_code(
            company,
            plant,
        )

        # -----------------------------------------------------
        # CREATE EMPLOYEE
        # -----------------------------------------------------

        employee = Employee.objects.create(
            employee_code=employee_code,
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            middle_name=validated_data.get("middle_name", ""),
            last_name=validated_data.get("last_name", ""),
            email=validated_data.get("email"),
            phone=validated_data.get("phone", "").strip(),
            company=company,
            plant=plant,
            department=department,
            employment_type=validated_data["employment_type"],
            joining_date=validated_data["joining_date"],
            status="active"
            if validated_data.get("is_active", True)
            else "inactive",
            grade=validated_data.get("grade"),
            designation=validated_data.get("designation"),
            location=validated_data.get("location"),
        )

        # -----------------------------------------------------
        # EMPLOYEE PROFILE
        # -----------------------------------------------------

        EmployeeProfile.objects.create(
            employee=employee,
            marital_status=validated_data.get("marital_status"),
            partner_name=validated_data.get("partner_name"),
            current_address=validated_data.get("current_address"),
            permanent_address=validated_data.get("permanent_address"),
            date_of_birth=validated_data.get("dob"),
            blood_group=validated_data.get("blood_group"),
            doctor_name=validated_data.get("doctor_name"),
            doctor_address=validated_data.get("doctor_address"),
            doctor_phone=(
                validated_data.get("doctor_phone_no") or ""
            ).strip(),
            health_issues=validated_data.get("health_issues"),
            qualification=validated_data.get("qualification"),
            experience=validated_data.get("experience"),
            employer_name=validated_data.get("employer_name"),
            employer_address=validated_data.get("employer_address"),
        )

        # -----------------------------------------------------
        # STATUTORY
        # -----------------------------------------------------

        EmployeeStatutory.objects.create(
            employee=employee,
            ppf_account_no=validated_data.get("ppf_account_no"),
            uan_no=validated_data.get("uan_no"),
            esic_no=validated_data.get("esic_no"),
            aadhaar_no=validated_data.get("aadhaar_no"),
            pan_no=validated_data.get("pan_no"),
            punching_code=validated_data.get("punching_code"),
        )

        # -----------------------------------------------------
        # EMERGENCY CONTACT
        # -----------------------------------------------------

        emergency_name = validated_data.get(
            "emergency_contact_name"
        )
        emergency_phone = (
            validated_data.get("emergency_contact_no") or ""
        ).strip()

        if emergency_name or emergency_phone:
            EmployeeEmergencyContact.objects.create(
                employee=employee,
                name=emergency_name or "",
                phone=emergency_phone or "",
            )

        # -----------------------------------------------------
        # CREATE USER
        # -----------------------------------------------------

        user = User.objects.create_user(
            # username=validated_data["username"],
            email=validated_data.get("email"),
            password=password,
            first_name=validated_data["first_name"],
            last_name=validated_data.get("last_name", ""),
            employee=employee,
            company=company,
            plant=plant,
            department=department,
            scope=validated_data.get("scope", "plant"),
            is_active=validated_data.get("is_active", True),
        )

        # -----------------------------------------------------
        # AUDIT FIELDS
        # -----------------------------------------------------

        if hasattr(user, "created_by") and request:
            user.created_by = request

        if hasattr(user, "updated_by") and request:
            user.updated_by = request

        if hasattr(user, "is_deleted"):
            user.is_deleted = False

        user.save(
            update_fields=[
                field
                for field in [
                    "created_by",
                    "updated_by",
                    "is_deleted",
                ]
                if hasattr(user, field)
            ]
        )

        # -----------------------------------------------------
        # ROLE ASSIGNMENT
        #
        # This is NOT permission management.
        # -----------------------------------------------------

        user_roles = [
            UserRole(
                user=user,
                role=role,
            )
            for role in roles
        ]

        if user_roles:
            UserRole.objects.bulk_create(user_roles)

        # -----------------------------------------------------
        # DOCUMENTS
        # -----------------------------------------------------

        for uploaded_file in documents:
            EmployeeDocument.objects.create(
                employee=employee,
                file=uploaded_file,
                original_file_name=getattr(
                    uploaded_file,
                    "name",
                    "",
                ),
            )

        return user


# =============================================================
# USER DETAIL SERIALIZER
# =============================================================

class UserSerializer(serializers.ModelSerializer):
    

    username = serializers.CharField(
        source="employee.username",
        read_only=True,
        allow_null=True,
    )

    employee_id = serializers.UUIDField(
        source="employee.id",
        read_only=True,
        allow_null=True,
    )

    employee_code = serializers.CharField(
        source="employee.employee_code",
        read_only=True,
        allow_null=True,
    )

    first_name = serializers.CharField(
        source="employee.first_name",
        read_only=True,
    )

    middle_name = serializers.CharField(
        source="employee.middle_name",
        read_only=True,
        allow_null=True,
    )

    last_name = serializers.CharField(
        source="employee.last_name",
        read_only=True,
    )

    phone = serializers.CharField(
        source="employee.phone",
        read_only=True,
        allow_null=True,
    )

    joining_date = serializers.DateField(
        source="employee.joining_date",
        read_only=True,
        allow_null=True,
    )

    employment_type = serializers.CharField(
        source="employee.employment_type",
        read_only=True,
    )

    grade = serializers.CharField(
        source="employee.grade",
        read_only=True,
        allow_null=True,
    )

    designation = serializers.CharField(
        source="employee.designation",
        read_only=True,
        allow_null=True,
    )

    location = serializers.CharField(
        source="employee.location",
        read_only=True,
        allow_null=True,
    )

    marital_status = serializers.CharField(
        source="employee.profile.marital_status",
        read_only=True,
        allow_null=True,
    )

    partner_name = serializers.CharField(
        source="employee.profile.partner_name",
        read_only=True,
        allow_null=True,
    )

    current_address = serializers.CharField(
        source="employee.profile.current_address",
        read_only=True,
        allow_null=True,
    )

    permanent_address = serializers.CharField(
        source="employee.profile.permanent_address",
        read_only=True,
        allow_null=True,
    )

    dob = serializers.DateField(
        source="employee.profile.date_of_birth",
        read_only=True,
        allow_null=True,
    )

    blood_group = serializers.CharField(
        source="employee.profile.blood_group",
        read_only=True,
        allow_null=True,
    )

    doctor_name = serializers.CharField(
        source="employee.profile.doctor_name",
        read_only=True,
        allow_null=True,
    )

    doctor_address = serializers.CharField(
        source="employee.profile.doctor_address",
        read_only=True,
        allow_null=True,
    )

    doctor_phone_no = serializers.CharField(
        source="employee.profile.doctor_phone",
        read_only=True,
        allow_null=True,
    )

    health_issues = serializers.CharField(
        source="employee.profile.health_issues",
        read_only=True,
        allow_null=True,
    )

    qualification = serializers.CharField(
        source="employee.profile.qualification",
        read_only=True,
        allow_null=True,
    )

    experience = serializers.DecimalField(
        source="employee.profile.experience",
        max_digits=6,
        decimal_places=2,
        read_only=True,
        allow_null=True,
    )

    employer_name = serializers.CharField(
        source="employee.profile.employer_name",
        read_only=True,
        allow_null=True,
    )

    employer_address = serializers.CharField(
        source="employee.profile.employer_address",
        read_only=True,
        allow_null=True,
    )

    ppf_account_no = serializers.CharField(
        source="employee.statutory.ppf_account_no",
        read_only=True,
        allow_null=True,
    )

    uan_no = serializers.CharField(
        source="employee.statutory.uan_no",
        read_only=True,
        allow_null=True,
    )

    esic_no = serializers.CharField(
        source="employee.statutory.esic_no",
        read_only=True,
        allow_null=True,
    )

    punching_code = serializers.CharField(
        source="employee.statutory.punching_code",
        read_only=True,
        allow_null=True,
    )

    aadhaar_no = serializers.CharField(
        source="employee.statutory.aadhaar_no",
        read_only=True,
        allow_null=True,
    )

    pan_no = serializers.CharField(
        source="employee.statutory.pan_no",
        read_only=True,
        allow_null=True,
    )

    company_id = serializers.UUIDField(
        source="company.id",
        read_only=True,
        allow_null=True,
    )

    plant_id = serializers.UUIDField(
        source="plant.id",
        read_only=True,
        allow_null=True,
    )

    department_id = serializers.UUIDField(
        source="department.id",
        read_only=True,
        allow_null=True,
    )

    roles = serializers.SerializerMethodField()
    # emergency_contact = serializers.SerializerMethodField()
    emergency_contact_name = serializers.SerializerMethodField()
    emergency_contact_no = serializers.SerializerMethodField()
    
    
    documents = serializers.SerializerMethodField()
    shift = serializers.SerializerMethodField()

    created_at = serializers.DateTimeField(
        source="employee.created_at",
        read_only=True,
    )

    updated_at = serializers.DateTimeField(
        source="employee.updated_at",
        read_only=True,
    )
    password = serializers.SerializerMethodField()
    def get_password(self, obj):

        if not obj.encrypted_password:
            return None

        try:
            return PasswordEncryptionService.decrypt(
                obj.encrypted_password
            )
        except Exception:
            return None
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    updated_by_name = serializers.SerializerMethodField()
    def _get_user_display_name(self, user):

        if not user:
            return None

        name = (
            f"{user.first_name or ''} "
            f"{user.last_name or ''}"
        ).strip()

        if name:
            return name

        if getattr(user, "employee", None):
            employee = user.employee

            name = (
                f"{employee.first_name or ''} "
                f"{employee.last_name or ''}"
            ).strip()

            if name:
                return name

        return user.email

    def get_created_by_name(self, obj):
            return self._get_user_display_name(
                obj.created_by
            )


    def get_updated_by_name(self, obj):
            return self._get_user_display_name(
                obj.updated_by
            )
    is_deleted = serializers.BooleanField(
        read_only=True
    )

    class Meta:
        model = User

        fields = [
            "id",
            "employee_id",
            "employee_code",
            "username",

            "first_name",
            "middle_name",
            "last_name",
            "email",
            "phone",

            "company_id",
            "plant_id",
            "department_id",
            "scope",

            "marital_status",
            "partner_name",
            "current_address",
            "permanent_address",
            "dob",
            "blood_group",
            "doctor_name",
            "doctor_address",
            "doctor_phone_no",
            "health_issues",

            "emergency_contact_name",
            "emergency_contact_no",

            "joining_date",
            "grade",
            "designation",
            "location",
            "qualification",
            "experience",
            "employer_name",
            "employer_address",

            "ppf_account_no",
            "uan_no",
            "esic_no",
            "punching_code",
            "aadhaar_no",
            "pan_no",

            "employment_type",
            "shift",

            "documents",

            "is_active",
            "is_deleted",

            "created_at",
            "updated_at",
            "password",
            "created_by",
            "updated_by",
            "created_by_name",
            "updated_by_name",

            "roles",
        ]
    def get_emergency_contact_name(self, obj):

        contact = (
            obj.employee.emergency_contacts
            .all()
            .first()
        )

        if not contact:
            return None

        return contact.name
    
    def get_emergency_contact_no(self, obj):
        contact = (
            obj.employee.emergency_contacts
            .all()
            .first()
        )

        if not contact:
            return None

        return contact.phone
            
    def get_documents(self, obj):
        request = self.context.get("request")
        return [
            {
                "id": str(document.id),
                "document_type": document.document_type,
                "file": (
                    document.file.url
                    if document.file
                    else None
                ),
                "original_file_name":
                    document.original_file_name,
                "document_url": (
                    request.build_absolute_uri(
                        reverse(
                            "employee-document-view",
                            kwargs={"document_id": document.id},
                        )
                    )
                    if request
                    else reverse(
                        "employee-document-view",
                        kwargs={"document_id": document.id},
                    )
                ),
                "created_at":
                    document.created_at,
                "updated_at":
                    document.updated_at,
            }
            for document in obj.employee.documents.all()
        ]

    # def get_shift(self, obj):
    #     assignment = (
    #         obj.employee.shift_assignments
    #         .filter(is_active=True)
    #         .select_related("shift")
    #         .first()
    #     )

    #     if not assignment or not assignment.shift:
    #         return None

    #     shift = assignment.shift

    #     return {
    #         "id": str(shift.id),
    #         "shift_type": shift.shift_type,
    #         "start_time": shift.start_time,
    #         "end_time": shift.end_time,
    #     }
    def get_shift(self, obj):

        assignment = (
            obj.employee.shift_assignments
            .filter(is_active=True)
            .select_related(
                "shift",
                "shift__company",
                "shift__plant",
            )
            .first()
        )

        if not assignment or not assignment.shift:
            return None

        shift = assignment.shift

        return {
            "id": str(shift.id),
            "shift_name": shift.name,
            "shift_code": shift.code,
            "shift_type": shift.shift_type,
            "shift_start_time": shift.start_time,
            "shift_end_time": shift.end_time,
            "shift_company_id": str(shift.company_id),
            "shift_plant_id": str(shift.plant_id),
            "shift_company_name": (
                shift.company.name
                if shift.company
                else None
            ),
            "shift_plant_name": (
                shift.plant.name
                if shift.plant
                else None
            ),
            "effective_from": assignment.effective_from,
            "effective_to": assignment.effective_to,
            "is_active": assignment.is_active,
        }

    def get_created_by(self, obj):
        if not obj.created_by:
            return None

        return {
            "id": str(obj.created_by.id),
            "email": obj.created_by.email,
        }

    def get_updated_by(self, obj):
        if not obj.updated_by:
            return None

        return {
            "id": str(obj.updated_by.id),
            "email": obj.updated_by.email,
        }

    # def get_roles(self, obj):
    #     return [
    #         {
    #             "id": str(item.role.id),
    #             "name": item.role.name,
    #             "code": item.role.code,
    #             "scope": item.role.scope,
    #         }
    #         for item in obj.assigned_roles.select_related(
    #             "role"
    #         ).all()
    #         if item.role
    #     ]
    def get_roles(self, obj):

        result = []

        user_roles = (
            obj.assigned_roles
            .select_related("role")
            .prefetch_related(
                "role__role_permissions__permission"
            )
            .all()
        )

        for item in user_roles:

            role = item.role

            if not role:
                continue

            permissions = []

            role_permissions = (
                RolePermission.objects
                .filter(
                    role=role
                )
                .select_related("permission")
            )

            for role_permission in role_permissions:

                permission = role_permission.permission

                if not permission:
                    continue

                permissions.append({
                    "id": str(permission.id),
                    "code": permission.code,
                    "module": permission.module,
                    "tab": permission.tab,
                    "action": permission.action,
                    "scope": permission.scope,
                    "description": permission.description,
                })

            result.append({
                "id": str(role.id),
                "name": role.name,
                "code": role.code,
                "scope": role.scope,
                "is_active": role.is_active,
                "permissions": permissions,
            })

        return result

# =============================================================
# USER UPDATE SERIALIZER
# =============================================================

class RepeatedListField(serializers.ListField):

    def get_value(self, dictionary):
        if hasattr(dictionary, "getlist"):
            values = dictionary.getlist(self.field_name)
            if values:
                return values
        return super().get_value(dictionary)


class UserUpdateSerializer(serializers.Serializer):

    username = serializers.CharField(
        max_length=100,
        required=False,
    )

    # password = serializers.CharField(
    #     write_only=True,
    #     min_length=8,
    #     required=False,
    # )

    first_name = serializers.CharField(
        max_length=100,
        required=False,
    )

    middle_name = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    last_name = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    email = serializers.EmailField(
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    phone = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    marital_status = serializers.CharField(
        max_length=50,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    partner_name = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    current_address = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    permanent_address = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    dob = serializers.DateField(
        required=False,
        allow_null=True,
    )

    blood_group = serializers.CharField(
        max_length=10,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    doctor_name = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    doctor_address = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    doctor_phone_no = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    health_issues = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    emergency_contact_name = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    emergency_contact_no = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    joining_date = serializers.DateField(
        required=False,
        allow_null=True,
    )

    grade = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    department = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    designation = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    location = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    qualification = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    experience = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        required=False,
        allow_null=True,
    )

    employer_name = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    employer_address = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    ppf_account_no = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    uan_no = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    esic_no = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    punching_code = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    aadhaar_no = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    pan_no = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    employment_type = serializers.ChoiceField(
        choices=Employee.EMPLOYMENT_TYPE_CHOICES,
        required=False,
    )

    shift_id = serializers.UUIDField(
        required=False,
        allow_null=True,
    )

    shift_name = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    shift_type = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    shift_start_time = serializers.TimeField(
        required=False,
        allow_null=True,
    )

    shift_end_time = serializers.TimeField(
        required=False,
        allow_null=True,
    )

    company = serializers.UUIDField(
        required=False,
        allow_null=True,
    )

    plant = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    scope = serializers.ChoiceField(
        choices=("company", "plant", "department"),
        required=False,
    )

    is_active = serializers.BooleanField(
        required=False,
    )

    role_ids = serializers.ListField(
        child=serializers.UUIDField(),
        required=False,
        allow_empty=True,
    )
    # =========================================================
# DOCUMENTS TO DELETE
# =========================================================

    document_ids_to_delete = RepeatedListField(
        child=serializers.UUIDField(),
        required=False,
        allow_empty=True,
    )

    documents = RepeatedListField(
        child=serializers.FileField(),
        required=False,
        allow_empty=True,
        write_only=True,
    )
    def validate(self, attrs):
        user = self.instance
   
        if not user:
            raise serializers.ValidationError(
                {"user": "User instance is required."}
            )

        employee = user.employee
        # -----------------------------------------------------
# PASSWORD CANNOT BE EDITED
# -----------------------------------------------------

        if "password" in self.initial_data:
            raise serializers.ValidationError({
                "password":
                    "Password cannot be edited from the User Edit API."
            })

        # -----------------------------------------------------
        # USERNAME
        # -----------------------------------------------------

        if "username" in attrs:
            username = attrs["username"].strip()

            if not username:
                raise serializers.ValidationError(
                    {"username": "Username cannot be empty."}
                )

            if Employee.objects.filter(
                username__iexact=username
            ).exclude(
                id=employee.id if employee else None
            ).exists():
                raise serializers.ValidationError(
                    {
                        "username":
                            "Employee with this username already exists."
                    }
                )

            # if User.objects.filter(
            #     username__iexact=username
            # ).exclude(
            #     id=user.id
            # ).exists():
            #     raise serializers.ValidationError(
            #         {
            #             "username":
            #                 "User with this username already exists."
            #         }
            #     )

            attrs["username"] = username

        # -----------------------------------------------------
        # EMAIL
        # -----------------------------------------------------

        if "email" in attrs:
            email = attrs["email"]

            if email:
                email = email.strip().lower()
                attrs["email"] = email

                if User.objects.filter(
                    email__iexact=email
                ).exclude(id=user.id).exists():
                    raise serializers.ValidationError(
                        {
                            "email":
                                "User with this email already exists."
                        }
                    )

                if employee and Employee.objects.filter(
                    email__iexact=email
                ).exclude(id=employee.id).exists():
                    raise serializers.ValidationError(
                        {
                            "email":
                                "Employee with this email already exists."
                        }
                    )
        # -----------------------------------------------------
        # PHONE NUMBER VALIDATION
        # User phone, emergency contact phone and doctor phone
        # must all be different.
        # -----------------------------------------------------

        current_employee_phone = (
            employee.phone or ""
        ).strip()

        current_doctor_phone = ""

        if hasattr(employee, "profile") and employee.profile:
            current_doctor_phone = (
                employee.profile.doctor_phone or ""
            ).strip()

        current_emergency_phone = ""

        emergency_contact = (
            employee.emergency_contacts
            .all()
            .first()
        )

        if emergency_contact:
            current_emergency_phone = (
                emergency_contact.phone or ""
            ).strip()


        # Use new value if provided.
        # Otherwise use existing database value.

        phone = (
            attrs["phone"].strip()
            if "phone" in attrs and attrs["phone"]
            else current_employee_phone
        )

        doctor_phone = (
            attrs["doctor_phone_no"].strip()
            if (
                "doctor_phone_no" in attrs
                and attrs["doctor_phone_no"]
            )
            else current_doctor_phone
        )

        emergency_phone = (
            attrs["emergency_contact_no"].strip()
            if (
                "emergency_contact_no" in attrs
                and attrs["emergency_contact_no"]
            )
            else current_emergency_phone
        )


        # Store cleaned values when they were supplied.

        if "phone" in attrs:
            attrs["phone"] = phone

        if "doctor_phone_no" in attrs:
            attrs["doctor_phone_no"] = doctor_phone

        if "emergency_contact_no" in attrs:
            attrs["emergency_contact_no"] = emergency_phone


        # -----------------------------------------------------
        # USER PHONE vs EMERGENCY PHONE
        # -----------------------------------------------------

        if (
            phone
            and emergency_phone
            and phone == emergency_phone
        ):
            raise serializers.ValidationError(
                {
                    "emergency_contact_no":
                        "Emergency contact number must be different "
                        "from user phone number."
                }
            )


        # -----------------------------------------------------
        # USER PHONE vs DOCTOR PHONE
        # -----------------------------------------------------

        if (
            phone
            and doctor_phone
            and phone == doctor_phone
        ):
            raise serializers.ValidationError(
                {
                    "doctor_phone_no":
                        "Doctor phone number must be different "
                        "from user phone number."
                }
            )


        # -----------------------------------------------------
        # EMERGENCY PHONE vs DOCTOR PHONE
        # -----------------------------------------------------

        if (
            emergency_phone
            and doctor_phone
            and emergency_phone == doctor_phone
        ):
            raise serializers.ValidationError(
                {
                    "doctor_phone_no":
                        "Doctor phone number must be different "
                        "from emergency contact number."
                }
            )
        # -----------------------------------------------------
        # ORGANIZATION
        # -----------------------------------------------------

        company_id = attrs.get(
            "company",
            user.company_id,
        )

        plant_value = attrs.get(
            "plant",
            user.plant_id,
        )

        department_value = attrs.get(
            "department",
            user.department_id,
        )

        plant_id = _optional_uuid(plant_value, "plant")
        department_id = _optional_uuid(
            department_value,
            "department",
        )

        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            raise serializers.ValidationError(
                {"company": "Company not found."}
            )

        plant = None

        if plant_id:
            try:
                plant = Plant.objects.get(
                    id=plant_id,
                    company=company,
                )
            except Plant.DoesNotExist:
                raise serializers.ValidationError(
                    {
                        "plant":
                            "Plant does not belong to selected company."
                    }
                )

        department = None

        if department_id:
            if not plant:
                raise serializers.ValidationError(
                    {
                        "department":
                            "Plant is required when department is selected."
                    }
                )

            try:
                department = Department.objects.get(
                    id=department_id,
                    plant=plant,
                )
            except Department.DoesNotExist:
                raise serializers.ValidationError(
                    {
                        "department":
                            "Department does not belong to selected plant."
                    }
                )

        attrs["company"] = company.id if company else None
        attrs["plant"] = plant.id if plant else None
        attrs["department"] = department.id if department else None
        # -----------------------------------------------------
# SHIFT VALIDATION
# -----------------------------------------------------

        shift_id = attrs.get("shift_id")

        if shift_id:
            shift = _validate_user_shift(
                shift_id=shift_id,
                company=company,
                plant=plant,
                shift_name=attrs.get("shift_name"),
                shift_type=attrs.get("shift_type"),
                shift_start_time=attrs.get("shift_start_time"),
                shift_end_time=attrs.get("shift_end_time"),
            )

            attrs["shift"] = shift
        # -----------------------------------------------------
        # SCOPE
        # -----------------------------------------------------

        scope = attrs.get(
            "scope",
            getattr(user, "scope", None) or "plant",
        )

        if scope == "plant" and not plant:
            raise serializers.ValidationError(
                {
                    "plant":
                        "Plant is required when scope is plant."
                }
            )

        if scope == "department":
            if not plant:
                raise serializers.ValidationError(
                    {
                        "plant":
                            "Plant is required when scope is department."
                    }
                )

            if not department:
                raise serializers.ValidationError(
                    {
                        "department":
                            "Department is required when scope is department."
                    }
                )

        attrs["scope"] = scope

        # -----------------------------------------------------
        # ROLE VALIDATION
        # -----------------------------------------------------

        if "role_ids" in attrs:

            role_ids = attrs["role_ids"]

            roles = list(
                Role.objects.filter(
                    id__in=role_ids,
                    is_active=True,
                ).select_related(
                    "company",
                    "plant",
                    "department",
                )
            )

            if len(roles) != len(set(role_ids)):
                raise serializers.ValidationError(
                    {
                        "role_ids":
                            "One or more roles are invalid."
                    }
                )

            for role in roles:

                if role.scope == "company":

                    if role.company_id != company.id:
                        raise serializers.ValidationError(
                            {
                                "role_ids":
                                    f"Role '{role.name}' does not belong "
                                    "to selected company."
                            }
                        )

                elif role.scope == "plant":

                    if not plant:
                        raise serializers.ValidationError(
                            {
                                "plant":
                                    f"Plant is required for role "
                                    f"'{role.name}'."
                            }
                        )

                    if (
                        role.company_id != company.id
                        or role.plant_id != plant.id
                    ):
                        raise serializers.ValidationError(
                            {
                                "role_ids":
                                    f"Role '{role.name}' does not belong "
                                    "to selected plant."
                            }
                        )

                elif role.scope == "department":

                    if not department:
                        raise serializers.ValidationError(
                            {
                                "department":
                                    f"Department is required for role "
                                    f"'{role.name}'."
                            }
                        )

                    if (
                        role.company_id != company.id
                        or role.plant_id != plant.id
                        or role.department_id != department.id
                    ):
                        raise serializers.ValidationError(
                            {
                                "role_ids":
                                    f"Role '{role.name}' does not belong "
                                    "to selected department."
                            }
                        )

                else:
                    raise serializers.ValidationError(
                        {
                            "role_ids":
                                f"Role '{role.name}' has unsupported scope "
                                f"'{role.scope}'."
                        }
                    )

            attrs["roles"] = roles
        return attrs


# =============================================================
# USER LIST SERIALIZER
# =============================================================

class UserListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source="employee.username",
        read_only=True,
        allow_null=True,
    )
    company_id = serializers.UUIDField(
        source="company.id",
        read_only=True,
        allow_null=True,
    )

    company_name = serializers.CharField(
        source="company.name",
        read_only=True,
        allow_null=True,
    )

    plant_id = serializers.UUIDField(
        source="plant.id",
        read_only=True,
        allow_null=True,
    )

    plant_name = serializers.CharField(
        source="plant.name",
        read_only=True,
        allow_null=True,
    )

    department_id = serializers.UUIDField(
        source="department.id",
        read_only=True,
        allow_null=True,
    )

    department_name = serializers.CharField(
        source="department.name",
        read_only=True,
        allow_null=True,
    )

    employee_id = serializers.UUIDField(
        source="employee.id",
        read_only=True,
        allow_null=True,
    )

    employee_code = serializers.CharField(
        source="employee.employee_code",
        read_only=True,
        allow_null=True,
    )
    punching_code = serializers.CharField(
        source="employee.statutory.punching_code",
        read_only=True,
        allow_null=True,
    )
    employee_name = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()
    shift_id = serializers.SerializerMethodField()
    shift_type = serializers.SerializerMethodField()
    shift_name = serializers.SerializerMethodField()
    shift_time = serializers.SerializerMethodField()

    class Meta:
        model = User

        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "employee_id",
            "employee_code",
            "punching_code",
            "employee_name",
            "company_id",
            "company_name",
            "plant_id",
            "plant_name",
            "department_id",
            "department_name",
            "scope",
            "roles",
            "shift_id",
            "shift_type",
            "shift_name",
            "shift_time",
            "is_active",
            "is_staff",
            "is_superuser",
        ]

    def get_full_name(self, obj):
        return (
            f"{obj.first_name or ''} "
            f"{obj.last_name or ''}"
        ).strip()

    def get_employee_name(self, obj):
        if not obj.employee:
            return None

        return (
            f"{obj.employee.first_name or ''} "
            f"{obj.employee.last_name or ''}"
        ).strip()

    def get_roles(self, obj):
        result = []

        for user_role in obj.assigned_roles.select_related("role").all():
            role = user_role.role

            if not role:
                continue

            result.append(
                {
                    "id": str(role.id),
                    "name": role.name,
                    "code": role.code,
                    "scope": getattr(role, "scope", None),
                    "is_active": getattr(
                        role,
                        "is_active",
                        True,
                    ),
                }
            )
        return result

    def _get_user_shift(self, obj):
        if not obj.employee:
            return None

        assignment = (
            obj.employee.shift_assignments
            .filter(
                is_active=True,
                shift__is_active=True,
                shift__is_deleted=False,
            )
            .select_related("shift")
            .order_by("-effective_from")
            .first()
        )

        if not assignment:
            return None

        return assignment.shift


    def get_shift_id(self, obj):
        shift = self._get_user_shift(obj)

        if not shift:
            return None

        return str(shift.id)


    def get_shift_type(self, obj):
        shift = self._get_user_shift(obj)

        if not shift:
            return None

        return shift.shift_type


    def get_shift_name(self, obj):
        shift = self._get_user_shift(obj)

        if not shift:
            return None

        return shift.name


    def get_shift_time(self, obj):
        shift = self._get_user_shift(obj)

        if not shift:
            return None

        if not shift.start_time or not shift.end_time:
            return None

        return (
            f"{shift.start_time.strftime('%H:%M')}-"
            f"{shift.end_time.strftime('%H:%M')}"
        )
        return result
