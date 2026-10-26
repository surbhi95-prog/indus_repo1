# # apps/accounts/services/user_service.py

# from django.db import transaction
# from django.contrib.auth import get_user_model

# from rest_framework.exceptions import ValidationError

# from apps.accounts.models.user_role import UserRole


# User = get_user_model()


# class UserService:

#     @staticmethod
#     @transaction.atomic
#     def create_user(validated_data):

#         employee = validated_data["employee"]
#         roles = validated_data["roles"]
#         password = validated_data["password"]

#         # -----------------------------------------
#         # Create User
#         # -----------------------------------------

#         user = User.objects.create_user(
#             email=employee.email,
#             password=password,
#             first_name=employee.first_name,
#             last_name=employee.last_name or "",
#             employee=employee,

#             # -------------------------------------
#             # Copy organizational context
#             # -------------------------------------

#             company=employee.company,
#             plant=employee.plant,
#             department=employee.department,

#             is_active=True,
#         )

#         # -----------------------------------------
#         # Assign Roles
#         # -----------------------------------------

#         user_roles = []

#         for role in roles:

#             user_roles.append(
#                 UserRole(
#                     user=user,
#                     role=role
#                 )
#             )

#         UserRole.objects.bulk_create(
#             user_roles
#         )

#         return user




# from django.db import transaction
# from django.contrib.auth import get_user_model

# from apps.hrms.models.employee import Employee
# from apps.accounts.models.user_role import UserRole

# User = get_user_model()


# class UserService:

#     @staticmethod
#     @transaction.atomic
#     def create_user(validated_data):

#         roles = validated_data.pop("roles")
#         password = validated_data.pop("password")

#         # -----------------------------------------
#         # Create Employee
#         # -----------------------------------------

#         employee = Employee.objects.create(
#     employee_code=validated_data["employee_code"],
#     first_name=validated_data["first_name"],
#     last_name=validated_data.get("last_name", ""),

#     company_id=validated_data["company"],
#     plant_id=validated_data["plant"],
#     department_id=validated_data["department"],

#     employment_type=validated_data["employment_type"],
#     joining_date=validated_data["joining_date"],
#     status=validated_data["status"],

#     email=validated_data["email"],
#     phone=validated_data.get("phone", ""),
# )

#         # -----------------------------------------
#         # Create User
#         # -----------------------------------------

#         user = User.objects.create_user(
#             email=employee.email,
#             password=password,

#             first_name=employee.first_name,
#             last_name=employee.last_name or "",

#             employee=employee,

#             # -------------------------------------
#             # Organizational context
#             # -------------------------------------

#             company=employee.company,
#             plant=employee.plant,
#             department=employee.department,

#             is_active=True,
#         )

#         # -----------------------------------------
#         # Assign Roles
#         # -----------------------------------------

#         user_roles = []

#         for role in roles:
#             user_roles.append(
#                 UserRole(
#                     user=user,
#                     role=role
#                 )
#             )

#         UserRole.objects.bulk_create(user_roles)

#         return user
from rest_framework.exceptions import ValidationError
from apps.hrms.models.shift import Shift
from apps.hrms.shift_types import normalize_shift_type
from apps.hrms.models.employee_shift import EmployeeShift
from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import F, Q, Prefetch

from apps.hrms.models.employee import Employee
from apps.accounts.models.user_role import UserRole

from apps.accounts.services.password_encryption_service import (
    PasswordEncryptionService
)
from apps.hrms.models.employee_profile import EmployeeProfile
from apps.hrms.models.employee_statutory import EmployeeStatutory
from apps.hrms.models.emergency_contact import EmployeeEmergencyContact
from apps.hrms.models.employee_document import EmployeeDocument

from apps.hrms.services.employee_code_service import (
    generate_employee_code
)
User = get_user_model()


class UserService:

    # @staticmethod
    # @transaction.atomic
    # def create_user(validated_data):

    #     roles = validated_data.pop("roles")
    #     password = validated_data.pop("password")

    #     # -----------------------------------------
    #     # Create Employee
    #     # -----------------------------------------

    #     employee = Employee.objects.create(
    #         employee_code=validated_data["employee_code"],
    #         first_name=validated_data["first_name"],
    #         last_name=validated_data.get("last_name", ""),

    #         company_id=validated_data["company"],
    #         plant_id=validated_data["plant"],
    #         department_id=validated_data["department"],

    #         employment_type=validated_data["employment_type"],
    #         joining_date=validated_data["joining_date"],
    #         status=validated_data["status"],

    #         email=validated_data["email"],
    #         phone=validated_data.get("phone", ""),
    #     )
#chcek get user by id
    #     # -----------------------------------------
    #     # Create User
    #     # -----------------------------------------

    #     user = User.objects.create_user(
    #         email=employee.email,
    #         password=password,

    #         first_name=employee.first_name,
    #         last_name=employee.last_name or "",

    #         employee=employee,

    #         # -------------------------------------
    #         # Organizational context
    #         # -------------------------------------

    #         company=employee.company,
    #         plant=employee.plant,
    #         department=employee.department,

    #         is_active=True,
    #     )

    #     # -----------------------------------------
    #     # Assign Roles
    #     # -----------------------------------------

    #     user_roles = []

    #     for role in roles:
    #         user_roles.append(
    #             UserRole(
    #                 user=user,
    #                 role=role
    #             )
    #         )

    #     UserRole.objects.bulk_create(user_roles)

    #     return user

    # @staticmethod
    # @transaction.atomic
    # def create_user(validated_data):

    #     roles = validated_data.pop("roles")
    #     password = validated_data.pop("password", None)
    #     encrypted_password = (
    #     PasswordEncryptionService.encrypt(password)
    #     if password
    #     else None
    # )
    #     company_id = validated_data["company"]

    #     plant_id = validated_data.get("plant")
    #     department_id = validated_data.get("department")

    #     # Empty string protection
    #     if plant_id == "":
    #         plant_id = None

    #     if department_id == "":
    #         department_id = None

    #     # -----------------------------------------
    #     # Create Employee
    #     # -----------------------------------------

    #     employee = Employee.objects.create(
    #         employee_code=validated_data["employee_code"],

    #         username=validated_data["username"],

    #         first_name=validated_data["first_name"],

    #         last_name=validated_data.get(
    #         "last_name",
    #         ""
    #     ),
    #         company_id=company_id,

    #         plant_id=plant_id,

    #         department_id=department_id,

    #         employment_type=validated_data[
    #             "employment_type"
    #         ],

    #         joining_date=validated_data[
    #             "joining_date"
    #         ],

    #         status=validated_data["status"],

    #         email=validated_data["email"],

    #         phone=validated_data.get(
    #             "phone",
    #             ""
    #         ),
    #     )

    #     # -----------------------------------------
    #     # Create User
    #     # -----------------------------------------

    #     user = User.objects.create_user(
    #         email=employee.email,

    #         password=password,

    #         first_name=employee.first_name,

    #         last_name=employee.last_name or "",

    #         employee=employee,

    #         company=employee.company,

    #         plant=employee.plant,

    #         department=employee.department,

    #         is_active=True,
    #         encrypted_password=encrypted_password,
    #     )

    #     # -----------------------------------------
    #     # Assign Roles
    #     # -----------------------------------------

    #     user_roles = [
    #         UserRole(
    #             user=user,
    #             role=role
    #         )
    #         for role in roles
    #     ]

    #     UserRole.objects.bulk_create(
    #         user_roles
    #     )

    #     return user
    @staticmethod
    @transaction.atomic
    def create_user(validated_data, created_by=None, documents=None):

        roles = validated_data.pop("roles", [])

        password = validated_data.pop("password")

        documents = documents or validated_data.pop(
            "documents",
            []
        )
        if len(documents) > 4:
            raise ValidationError({
                "documents":
                    "Maximum 4 documents can be uploaded for a user."
            })
        company = validated_data.pop("company")

        plant = validated_data.pop(
            "plant",
            None
        )

        department = validated_data.pop(
            "department",
            None
        )

        # =====================================================
        # 1. GENERATE EMPLOYEE CODE
        # =====================================================

        employee_code = generate_employee_code(
            company,
            plant
        )

        # =====================================================
        # 2. CREATE EMPLOYEE
        # =====================================================

        employee = Employee.objects.create(
            employee_code=employee_code,

            username=validated_data["username"],

            first_name=validated_data["first_name"],

            middle_name=validated_data.get(
                "middle_name",
                ""
            ),

            last_name=validated_data.get(
                "last_name",
                ""
            ),

            email=validated_data.get(
                "email"
            ),

            phone=validated_data.get(
                "phone",
                ""
            ),

            company=company,

            plant=plant,

            department=department,

            employment_type=validated_data[
                "employment_type"
            ],

            joining_date=validated_data[
                "joining_date"
            ],

            status=(
                "active"
                if validated_data.get(
                    "is_active",
                    True
                )
                else "inactive"
            ),

            grade=validated_data.get(
                "grade"
            ),

            designation=validated_data.get(
                "designation"
            ),

            location=validated_data.get(
                "location"
            ),
        )

        # =====================================================
        # 3. CREATE EMPLOYEE PROFILE
        # =====================================================

        EmployeeProfile.objects.create(
            employee=employee,

            marital_status=validated_data.get(
                "marital_status"
            ),

            partner_name=validated_data.get(
                "partner_name"
            ),

            current_address=validated_data.get(
                "current_address"
            ),

            permanent_address=validated_data.get(
                "permanent_address"
            ),

            date_of_birth=validated_data.get(
                "dob"
            ),

            blood_group=validated_data.get(
                "blood_group"
            ),

            doctor_name=validated_data.get(
                "doctor_name"
            ),

            doctor_address=validated_data.get(
                "doctor_address"
            ),

            doctor_phone=validated_data.get(
                "doctor_phone_no"
            ),

            health_issues=validated_data.get(
                "health_issues"
            ),

            qualification=validated_data.get(
                "qualification"
            ),

            experience=validated_data.get(
                "experience"
            ),

            employer_name=validated_data.get(
                "employer_name"
            ),

            employer_address=validated_data.get(
                "employer_address"
            ),
        )

        # =====================================================
        # 4. CREATE STATUTORY INFORMATION
        # =====================================================

        EmployeeStatutory.objects.create(
            employee=employee,

            ppf_account_no=validated_data.get(
                "ppf_account_no"
            ),

            uan_no=validated_data.get(
                "uan_no"
            ),

            esic_no=validated_data.get(
                "esic_no"
            ),

            punching_code=validated_data.get(
                "punching_code"
            ),

            aadhaar_no=validated_data.get(
                "aadhaar_no"
            ),

            pan_no=validated_data.get(
                "pan_no"
            ),
        )

        # =====================================================
        # 5. CREATE EMERGENCY CONTACT
        # =====================================================

        emergency_name = validated_data.get(
            "emergency_contact_name"
        )

        emergency_phone = validated_data.get(
            "emergency_contact_no"
        )

        if emergency_name or emergency_phone:

            EmployeeEmergencyContact.objects.create(
                employee=employee,

                name=emergency_name or "",

                phone=emergency_phone or "",
            )

        # =====================================================
        # 6. CREATE USER
        # =====================================================

        user = User.objects.create_user(
            # username=validated_data["username"],

            email=validated_data.get(
                "email"
            ),

            password=password,

            first_name=validated_data[
                "first_name"
            ],

            last_name=validated_data.get(
                "last_name",
                ""
            ),

            employee=employee,

            company=company,

            plant=plant,

            department=department,

            scope=validated_data.get(
                "scope",
                "plant"
            ),

            is_active=validated_data.get(
                "is_active",
                True
            ),
        )
        # =====================================================
# ASSIGN SHIFT
# =====================================================

        shift = validated_data.get("shift")

        if not shift:
            raise ValidationError({
                "shift_id": "Shift is required for user."
            })

        if (
            shift.company_id != employee.company_id
            or shift.plant_id != employee.plant_id
        ):
            raise ValidationError({
                "shift_id":
                    "Selected shift does not belong to "
                    "the employee's company and plant."
            })

        EmployeeShift.objects.filter(
            employee=employee,
            is_active=True,
        ).update(
            is_active=False,
            effective_to=employee.joining_date,
        )

        EmployeeShift.objects.create(
            employee=employee,
            shift=shift,
            effective_from=employee.joining_date,
            is_active=True,
        )
        # -----------------------------------------------------
# ENCRYPTED PASSWORD
# -----------------------------------------------------

        user.encrypted_password = (
            PasswordEncryptionService.encrypt(password)
        )

        user.save(
            update_fields=[
                "encrypted_password",
            ]
        )
        # =====================================================
        # 7. AUDIT FIELDS
        # =====================================================

        # if hasattr(user, "created_by"):
        #     user.created_by = created_by

        # if hasattr(user, "updated_by"):
        #     user.updated_by = created_by

        # if hasattr(user, "is_deleted"):
        #     user.is_deleted = False

        # user.save()
        
        user.created_by = created_by
        user.updated_by = created_by
        user.is_deleted = False
        user.save(
            update_fields=[
                "created_by",
                "updated_by",
                "is_deleted",
            ]
        )
        # =====================================================
        # 8. ASSIGN ROLES
        # =====================================================

        user_roles = [
            UserRole(
                user=user,
                role=role
            )
            for role in roles
        ]

        if user_roles:

            UserRole.objects.bulk_create(
                user_roles
            )

        # =====================================================
        # 9. SAVE DOCUMENTS
        # =====================================================

        for uploaded_file in documents:

            EmployeeDocument.objects.create(
                employee=employee,

                file=uploaded_file,

                original_file_name=getattr(
                    uploaded_file,
                    "name",
                    ""
                ),
            )

        # =====================================================
        # 10. RETURN USER
        # =====================================================

        return user
    # =========================================================
    # GET USER ROLES
    # =========================================================

    @staticmethod
    def get_user_roles(user):

        return list(
            UserRole.objects
            .filter(user=user)
            .select_related("role")
        )

    # =========================================================
    # CHECK SUPER ADMIN
    # =========================================================

    @staticmethod
    def is_super_admin(user):

        if user.is_superuser:
            return True

        roles = UserService.get_user_roles(user)

        role_names = {
            item.role.name.strip().upper()
            for item in roles
            if item.role
        }

        role_codes = {
            item.role.code.strip().upper()
            for item in roles
            if item.role and item.role.code
        }

        return bool(
            role_names.intersection({
                "SA",
                "SUPER ADMIN",
                "SUPER_ADMIN",
                "SUPERADMIN",
            })
            or
            role_codes.intersection({
                "SA",
                "SUPER_ADMIN",
                "SUPERADMIN",
            })
        )

    # =========================================================
    # CHECK HR
    # =========================================================

    @staticmethod
    def is_hr(user):

        roles = UserService.get_user_roles(user)

        role_names = {
            item.role.name.strip().upper()
            for item in roles
            if item.role
        }

        role_codes = {
            item.role.code.strip().upper()
            for item in roles
            if item.role and item.role.code
        }

        return bool(
            role_names.intersection({
                "HR",
                "HR MANAGER",
                "HR_MANAGER",
                "PLANT HR",
                "PLANT_HR",
            })
            or
            role_codes.intersection({
                "HR",
                "HR_MANAGER",
                "PLANT_HR",
            })
        )

    # # =========================================================
    # # CHECK COMPANY ADMIN
    # # =========================================================

    # @staticmethod
    # def is_company_admin(user):

    #     roles = UserService.get_user_roles(user)

    #     role_names = {
    #         item.role.name.strip().upper()
    #         for item in roles
    #         if item.role
    #     }

    #     role_codes = {
    #         item.role.code.strip().upper()
    #         for item in roles
    #         if item.role and item.role.code
    #     }

    #     return bool(
    #         role_names.intersection({
    #             "COMPANY ADMIN",
    #             "COMPANY_ADMIN",
    #             "COMPANYADMIN",
    #         })
    #         or
    #         role_codes.intersection({
    #             "COMPANY_ADMIN",
    #             "COMPANYADMIN",
    #         })
    #     )

    # =========================================================
    # GET USERS
    # =========================================================

    # @staticmethod
    # def get_users(
    #     logged_in_user,
    #     company_id=None,
    #     plant_id=None,
    #     department_id=None,
    # ):

    #     queryset = (
    #         User.objects
    #         .select_related(
    #             "employee",
    #             "company",
    #             "plant",
    #             "department",
    #         )
    #         .prefetch_related(
    #             "assigned_roles__role"
    #         )
    #     )

    #     # =====================================================
    #     # SUPER ADMIN
    #     # =====================================================

    #     if UserService.is_super_admin(logged_in_user):

    #         # SA must have company
    #         if not logged_in_user.company_id:
    #             return User.objects.none()

    #         # SA can only see users
    #         # from his company
    #         queryset = queryset.filter(
    #             company_id=logged_in_user.company_id
    #         )

    #         # -----------------------------------------
    #         # Company filter
    #         # -----------------------------------------

    #         if company_id:

    #             # Don't allow SA to access
    #             # another company

    #             if str(company_id) != str(
    #                 logged_in_user.company_id
    #             ):
    #                 return User.objects.none()

    #             queryset = queryset.filter(
    #                 company_id=company_id
    #             )

    #         # -----------------------------------------
    #         # Plant filter
    #         # -----------------------------------------

    #         if plant_id:
    #             queryset = queryset.filter(
    #                 plant_id=plant_id
    #             )

    #         # -----------------------------------------
    #         # Department filter
    #         # -----------------------------------------

    #         if department_id:
    #             queryset = queryset.filter(
    #                 department_id=department_id
    #             )

    #         return queryset.order_by(
    #             "first_name",
    #             "last_name",
    #         )

    #     # =====================================================
    #     # HR
    #     # =====================================================

    #     if UserService.is_hr(logged_in_user):

    #         # HR must have company
    #         if not logged_in_user.company_id:
    #             return User.objects.none()

    #         # HR must have plant
    #         if not logged_in_user.plant_id:
    #             return User.objects.none()

    #         # -----------------------------------------
    #         # HR can ONLY see own company + own plant
    #         # -----------------------------------------

    #         queryset = queryset.filter(
    #             company_id=logged_in_user.company_id,
    #             plant_id=logged_in_user.plant_id,
    #         )

    #         # -----------------------------------------
    #         # Company filter
    #         # -----------------------------------------

    #         if company_id:

    #             if str(company_id) != str(
    #                 logged_in_user.company_id
    #             ):
    #                 return User.objects.none()

    #             queryset = queryset.filter(
    #                 company_id=company_id
    #             )

    #         # -----------------------------------------
    #         # Plant filter
    #         # -----------------------------------------

    #         if plant_id:

    #             if str(plant_id) != str(
    #                 logged_in_user.plant_id
    #             ):
    #                 return User.objects.none()

    #             queryset = queryset.filter(
    #                 plant_id=plant_id
    #             )

    #         # -----------------------------------------
    #         # Department filter
    #         # -----------------------------------------

    #         if department_id:
    #             queryset = queryset.filter(
    #                 department_id=department_id
    #             )

    #         return queryset.order_by(
    #             "first_name",
    #             "last_name",
    #         )

    #     # =====================================================
    #     # OTHER USERS
    #     # =====================================================

    #     return User.objects.none()

    # # =========================================================
    # # GET USER BY ID
    # # =========================================================

    # @staticmethod
    # def get_user_by_id(
    #     logged_in_user,
    #     user_id,
    # ):

    #     try:

    #         user = (
    #             User.objects
    #             .select_related(
    #                 "employee",
    #                 "company",
    #                 "plant",
    #                 "department",
    #             )
    #             .prefetch_related(
    #                 "assigned_roles__role"
    #             )
    #             .get(
    #                 id=user_id
    #             )
    #         )

    #     except User.DoesNotExist:

    #         return None

    #     # =====================================================
    #     # SUPER ADMIN
    #     # =====================================================

    #     if UserService.is_super_admin(logged_in_user):

    #         if not logged_in_user.company_id:
    #             return None

    #         if user.company_id != logged_in_user.company_id:
    #             return None

    #         return user

    #     # =====================================================
    #     # HR
    #     # =====================================================

    #     if UserService.is_hr(logged_in_user):

    #         if not logged_in_user.company_id:
    #             return None

    #         if not logged_in_user.plant_id:
    #             return None

    #         # Same company
    #         if user.company_id != logged_in_user.company_id:
    #             return None

    #         # Same plant
    #         if user.plant_id != logged_in_user.plant_id:
    #             return None

    #         return user

    #     # =====================================================
    #     # OTHER USERS
    #     # =====================================================

    #     return None

    @staticmethod
    def get_users(
        logged_in_user,
        company_id=None,
        plant_id=None,
        department_id=None,
        scope=None,
        employee_code=None,
        email=None,
        first_name=None,
        last_name=None,
        search=None,
        is_active=None,
        is_staff=None,
        is_superuser=None,
        role_id=None,
        shift_id=None,
        shift_type=None,
        is_deleted=False
    ):

        # -----------------------------------------------------
        # BASE QUERY
        # -----------------------------------------------------

        queryset = (
            User.objects
            .select_related(
                "employee",
                "company",
                "plant",
                "department",
            )
            .prefetch_related(
                "assigned_roles__role",
                Prefetch(
                    "employee__shift_assignments",
                    queryset=EmployeeShift.objects
                        .filter(
                            is_active=True,
                            shift__is_active=True,
                            shift__is_deleted=False,
                        )
                        .select_related("shift")
                        .order_by("-effective_from"),
                    to_attr="_user_list_shift_assignments",
                ),
            )
            .filter(
                is_deleted=False
            )
        )

        # =====================================================
        # SUPER ADMIN
        # =====================================================

        # if UserService.is_super_admin(logged_in_user):

        #     # -------------------------------------------------
        #     # If Super Admin has company assigned
        #     # restrict to that company.
        #     #
        #     # If Super Admin has NO company:
        #     # allow company filter to determine the company.
        #     # -------------------------------------------------

        #     if logged_in_user.company_id:

        #         queryset = queryset.filter(
        #             company_id=logged_in_user.company_id
        #         )

        #         # Requested company must match logged-in SA
        #         if company_id:

        #             if str(company_id) != str(
        #                 logged_in_user.company_id
        #             ):
        #                 return User.objects.none()

        #             queryset = queryset.filter(
        #                 company_id=company_id
        #             )

        #     else:

        #         # Global Super Admin
        #         if company_id:
        #             queryset = queryset.filter(
        #                 company_id=company_id
        #             )

        # # =====================================================
        # # HR / PLANT HR
        # # =====================================================

        # elif UserService.is_hr(logged_in_user):

        #     # -------------------------------------------------
        #     # HR must have company
        #     # -------------------------------------------------

        #     if not logged_in_user.company_id:
        #         return User.objects.none()

        #     # -------------------------------------------------
        #     # HR must have plant
        #     # -------------------------------------------------

        #     if not logged_in_user.plant_id:
        #         return User.objects.none()

        #     # -------------------------------------------------
        #     # HR can only see own company + own plant
        #     # -------------------------------------------------

        #     queryset = queryset.filter(
        #         company_id=logged_in_user.company_id,
        #         plant_id=logged_in_user.plant_id,
        #     )

        #     # -------------------------------------------------
        #     # Company validation
        #     # -------------------------------------------------

        #     if company_id:

        #         if str(company_id) != str(
        #             logged_in_user.company_id
        #         ):
        #             return User.objects.none()

        #     # -------------------------------------------------
        #     # Plant validation
        #     # -------------------------------------------------

        #     if plant_id:

        #         if str(plant_id) != str(
        #             logged_in_user.plant_id
        #         ):
        #             return User.objects.none()

        # # =====================================================
        # # OTHER USERS
        # # =====================================================

        # else:
        #     return User.objects.none()

        # =====================================================
        # ORGANIZATION FILTERS
        # =====================================================

        # -----------------------------------------------------
        # Company
        # -----------------------------------------------------

        if company_id:
            queryset = queryset.filter(
                company_id=company_id
            )

        # -----------------------------------------------------
        # Plant
        # -----------------------------------------------------

        if plant_id:
            queryset = queryset.filter(
                plant_id=plant_id
            )
        if scope:
            queryset = queryset.filter(
                scope__iexact=scope.strip()
            )

        # -----------------------------------------------------
        # Department
        # -----------------------------------------------------

        if department_id:
            queryset = queryset.filter(
                department_id=department_id
            )

        # =====================================================
        # EMPLOYEE FILTERS
        # =====================================================

        # -----------------------------------------------------
        # Employee Code
        # -----------------------------------------------------

        if employee_code:
            queryset = queryset.filter(
                employee__employee_code__icontains=employee_code
            )

        # -----------------------------------------------------
        # Email
        # -----------------------------------------------------

        if email:
            queryset = queryset.filter(
                email__icontains=email
            )

        # -----------------------------------------------------
        # First Name
        # -----------------------------------------------------

        if first_name:
            queryset = queryset.filter(
                first_name__icontains=first_name
            )

        # -----------------------------------------------------
        # Last Name
        # -----------------------------------------------------

        if last_name:
            queryset = queryset.filter(
                last_name__icontains=last_name
            )

        # =====================================================
        # SEARCH
        # =====================================================

        if search:

            queryset = queryset.filter(
                Q(first_name__icontains=search)
                |
                Q(last_name__icontains=search)
                |
                Q(email__icontains=search)
                |
                Q(employee__employee_code__icontains=search)
            )

        # =====================================================
        # STATUS FILTERS
        # =====================================================

        if is_active is not None:

            queryset = queryset.filter(
                is_active=is_active
            )

        if is_staff is not None:

            queryset = queryset.filter(
                is_staff=is_staff
            )

        if is_superuser is not None:

            queryset = queryset.filter(
                is_superuser=is_superuser
            )

        # =====================================================
        # ROLE FILTER
        # =====================================================

        if role_id:

            queryset = queryset.filter(
                assigned_roles__role_id=role_id
            )
        # =====================================================
# SHIFT FILTERS
        # =====================================================

        if shift_id:
            queryset = queryset.filter(
                employee__shift_assignments__shift_id=shift_id,
                employee__shift_assignments__is_active=True,
                employee__shift_assignments__shift__is_active=True,
                employee__shift_assignments__shift__is_deleted=False,
            )

        if shift_type:
            queryset = queryset.filter(
                employee__shift_assignments__shift__shift_type__iexact=normalize_shift_type(shift_type),
                employee__shift_assignments__is_active=True,
                employee__shift_assignments__shift__is_active=True,
                employee__shift_assignments__shift__is_deleted=False,
            )
                # =====================================================
        # REMOVE DUPLICATES
        # =====================================================

        queryset = queryset.distinct()

        # =====================================================
        # ORDER
        # =====================================================

        return queryset.order_by(
            F("employee__created_at").desc(nulls_last=True),
            "-pk",
        )



    

       # =========================================================
    # GET USER BY ID
    # =========================================================

    @staticmethod
    def get_user_by_id(logged_in_user, user_id):

        try:
            return (
                User.objects
                .select_related(
                    "employee",
                    "company",
                    "plant",
                    "department",
                    "employee__profile",
                    "employee__statutory",
                )
                .prefetch_related(
                    "assigned_roles__role",
                    "assigned_roles__role__role_permissions__permission",
                    "employee__emergency_contacts",
                    "employee__documents",
                    "employee__shift_assignments__shift",
                )
                .filter(
                    is_deleted=False
                )
                .get(
                    id=user_id
                )
            )

        except User.DoesNotExist:
            return None


    # =========================================================
    # UPDATE USER
    # =========================================================

    @staticmethod
    @transaction.atomic
    def update_user(
        user,
        validated_data,
        updated_by=None,
        documents=None,
    ):
        roles = validated_data.pop(
            "roles",
            None
        )

        validated_documents = validated_data.pop(
            "documents",
            [],
        )
        # The view supplies request.FILES.getlist("documents"), including an
        # empty list when no files were uploaded. Only fall back to serializer
        # files when no explicit file list was supplied; never merge/count
        # both representations of the same multipart uploads.
        document_source = (
            documents if documents is not None else validated_documents
        )
        documents = list({
            id(uploaded_file): uploaded_file
            for uploaded_file in document_source
        }.values())

        company = validated_data.pop(
            "company",
            None
        )

        plant = validated_data.pop(
            "plant",
            None
        )

        department = validated_data.pop(
            "department",
            None
        )

        scope = validated_data.pop(
            "scope",
            None
        )

        # password = validated_data.pop(
        #     "password",
        #     None
        # )

        username = validated_data.pop(
            "username",
            None
        )

        shift_id = validated_data.pop(
            "shift_id",
            None
        )

        # validated_data.pop(
        #     "shift_type",
        #     None
        # )

        # validated_data.pop(
        #     "shift_time",
        #     None
        # )

        employee = user.employee

        if not employee:
            raise ValueError(
                "User is not linked to an employee."
            )

        # ---------------------------------------------------------
        # USER
        # ---------------------------------------------------------

        for field in [
            "email",
            "first_name",
            "last_name",
            "is_active",
        ]:
            if field in validated_data:
                setattr(
                    user,
                    field,
                    validated_data[field],
                )
        password = validated_data.get("password")
        if password:
            user.set_password(password)

        if scope is not None:
            user.scope = scope

        if company is not None:
            user.company_id = company

        if plant is not None:
            user.plant_id = plant

        if department is not None:
            user.department_id = department

        if updated_by is not None:
            user.updated_by = updated_by

        user.save()

        # ---------------------------------------------------------
        # EMPLOYEE
        # ---------------------------------------------------------

        employee_fields = [
            "first_name",
            "middle_name",
            "last_name",
            "phone",
            "email",
            "employment_type",
            "joining_date",
            "grade",
            "designation",
            "location",
        ]

        for field in employee_fields:
            if field in validated_data:
                setattr(
                    employee,
                    field,
                    validated_data[field],
                )

        if username is not None:
            employee.username = username

        if company is not None:
            employee.company_id = company

        if plant is not None:
            employee.plant_id = plant

        if department is not None:
            employee.department_id = department

        employee.status = (
            "active"
            if user.is_active
            else "inactive"
        )

        employee.save()

        # ---------------------------------------------------------
        # PROFILE
        # ---------------------------------------------------------

        profile, _ = EmployeeProfile.objects.get_or_create(
            employee=employee
        )

        profile_fields = {
            "marital_status": "marital_status",
            "partner_name": "partner_name",
            "current_address": "current_address",
            "permanent_address": "permanent_address",
            "date_of_birth": "dob",
            "blood_group": "blood_group",
            "doctor_name": "doctor_name",
            "doctor_address": "doctor_address",
            "doctor_phone": "doctor_phone_no",
            "health_issues": "health_issues",
            "qualification": "qualification",
            "experience": "experience",
            "employer_name": "employer_name",
            "employer_address": "employer_address",
        }

        for model_field, request_field in profile_fields.items():
            if request_field in validated_data:
                setattr(
                    profile,
                    model_field,
                    validated_data[request_field],
                )

        profile.save()

        # ---------------------------------------------------------
        # STATUTORY
        # ---------------------------------------------------------

        statutory, _ = EmployeeStatutory.objects.get_or_create(
            employee=employee
        )

        statutory_fields = [
            "ppf_account_no",
            "uan_no",
            "esic_no",
            "punching_code",
            "aadhaar_no",
            "pan_no",
        ]

        for field in statutory_fields:
            if field in validated_data:
                setattr(
                    statutory,
                    field,
                    validated_data[field],
                )

        statutory.save()

        # ---------------------------------------------------------
        # EMERGENCY CONTACT
        # ---------------------------------------------------------

        emergency_name = validated_data.get(
            "emergency_contact_name"
        )

        emergency_phone = validated_data.get(
            "emergency_contact_no"
        )

        if (
            "emergency_contact_name" in validated_data
            or "emergency_contact_no" in validated_data
        ):
            emergency = (
                EmployeeEmergencyContact.objects
                .filter(employee=employee)
                .first()
            )

            if not emergency:
                emergency = EmployeeEmergencyContact(
                    employee=employee
                )

            emergency.name = (
                emergency_name
                if emergency_name is not None
                else emergency.name
                if emergency.pk
                else ""
            )

            emergency.phone = (
                emergency_phone
                if emergency_phone is not None
                else emergency.phone
                if emergency.pk
                else ""
            )

            emergency.save()

        # ---------------------------------------------------------
        # SHIFT
        # ---------------------------------------------------------

        # if shift_id is not None:
        #     from apps.hrms.models.shift import Shift
        #     from apps.hrms.models.employee_shift import EmployeeShift

        #     shift = Shift.objects.filter(
        #         id=shift_id,
        #         company_id=employee.company_id,
        #         plant_id=employee.plant_id,
        #         is_active=True,
        #         is_deleted=False,
        #     ).first()

        #     if not shift:
        #         raise ValueError(
        #             "Selected shift does not belong to "
        #             "the employee's company and plant."
        #         )

        #     EmployeeShift.objects.filter(
        #         employee=employee,
        #         is_active=True,
        #     ).update(
        #         is_active=False
        #     )

        #     EmployeeShift.objects.create(
        #         employee=employee,
        #         shift=shift,
        #         effective_from=employee.joining_date,
        #         is_active=True,
        #     )
        # ---------------------------------------------------------
# SHIFT
# ---------------------------------------------------------

        shift = validated_data.pop(
            "shift",
            None
        )

        if shift is not None:

            if (
                shift.company_id != employee.company_id
                or shift.plant_id != employee.plant_id
            ):
                raise ValidationError({
                    "shift_id":
                        "Selected shift does not belong to "
                        "the employee's company and plant."
                })

            from django.utils import timezone
            from datetime import timedelta

            current_assignment = (
                EmployeeShift.objects
                .filter(
                    employee=employee,
                    is_active=True,
                )
                .first()
            )

            effective_from = timezone.localdate()

            if current_assignment:

                current_assignment.is_active = False
                current_assignment.effective_to = (
                    effective_from - timedelta(days=1)
                )

                current_assignment.save(
                    update_fields=[
                        "is_active",
                        "effective_to",
                        "updated_at",
                    ]
                )

            EmployeeShift.objects.create(
                employee=employee,
                shift=shift,
                effective_from=effective_from,
                is_active=True,
            )
        # ---------------------------------------------------------
        # ROLES
        # ---------------------------------------------------------

        # ---------------------------------------------------------
# ROLES
# ---------------------------------------------------------

        if roles is not None:

            current_role_ids = set(
                UserRole.objects
                .filter(user=user)
                .values_list(
                    "role_id",
                    flat=True
                )
            )

            requested_role_ids = {
                role.id
                for role in roles
            }

            # -----------------------------------------------------
            # REMOVE ONLY USER ROLE ASSIGNMENTS
            # -----------------------------------------------------

            roles_to_remove = (
                current_role_ids
                - requested_role_ids
            )

            if roles_to_remove:

                UserRole.objects.filter(
                    user=user,
                    role_id__in=roles_to_remove,
                ).delete()

            # -----------------------------------------------------
            # ADD ONLY NEW USER ROLE ASSIGNMENTS
            # -----------------------------------------------------

            roles_to_add = (
                requested_role_ids
                - current_role_ids
            )

            if roles_to_add:

                UserRole.objects.bulk_create([
                    UserRole(
                        user=user,
                        role=role,
                    )
                    for role in roles
                    if role.id in roles_to_add
                ])
        # ---------------------------------------------------------
# DELETE DOCUMENTS
        # ---------------------------------------------------------

                # ---------------------------------------------------------
        # DOCUMENT UPDATE
        # ---------------------------------------------------------

        document_ids_to_delete = validated_data.pop(
            "document_ids_to_delete",
            []
        )

        documents = documents or []

        # ---------------------------------------------------------
        # DOCUMENTS ARE OPTIONAL
        # ---------------------------------------------------------
        #
        # If neither document deletion nor new documents are
        # requested, do nothing.
        #
        # This is important because existing users may already
        # have more than 4 documents in the database.
        #
        # Normal user edit must still work in that case.
        # ---------------------------------------------------------

        if document_ids_to_delete or documents:

            existing_documents = (
                EmployeeDocument.objects
                .filter(
                    employee=employee
                )
            )

            # -----------------------------------------------------
            # VALIDATE DOCUMENT IDs
            # -----------------------------------------------------

            documents_to_delete = (
                existing_documents
                .filter(
                    id__in=document_ids_to_delete
                )
            )

            found_ids = set(
                documents_to_delete.values_list(
                    "id",
                    flat=True
                )
            )

            requested_ids = set(
                document_ids_to_delete
            )

            missing_ids = (
                requested_ids - found_ids
            )

            if missing_ids:

                raise ValidationError({
                    "document_ids_to_delete":
                        "One or more documents do not belong "
                        "to this user."
                })

            # -----------------------------------------------------
            # CALCULATE FINAL DOCUMENT COUNT
            # -----------------------------------------------------

            current_document_count = (
                existing_documents.count()
            )

            # requested_ids is a set so repeated IDs remove/count only once.
            delete_count = len(requested_ids)

            new_document_count = len(
                documents
            )

            final_document_count = (
                current_document_count
                - delete_count
                + new_document_count
            )

            # -----------------------------------------------------
            # MAXIMUM 4 DOCUMENTS
            # -----------------------------------------------------

            if final_document_count > 4:

                raise ValidationError({
                    "documents": (
                        "Maximum 4 documents are allowed. "
                        f"Current documents: "
                        f"{current_document_count}, "
                        f"documents to delete: "
                        f"{delete_count}, "
                        f"new documents: "
                        f"{new_document_count}, "
                        f"final documents: "
                        f"{final_document_count}."
                    )
                })

            # -----------------------------------------------------
            # DELETE OLD DOCUMENTS
            # -----------------------------------------------------

            for document in documents_to_delete:

                if document.file:
                    storage = document.file.storage
                    file_name = document.file.name

                    transaction.on_commit(
                        lambda storage=storage, file_name=file_name: (
                            storage.delete(file_name)
                            if file_name
                            and not EmployeeDocument.objects.filter(
                                file=file_name
                            ).exists()
                            else None
                        )
                    )

                document.delete()

            # -----------------------------------------------------
            # ADD NEW DOCUMENTS
            # -----------------------------------------------------

            for uploaded_file in documents:

                EmployeeDocument.objects.create(
                    employee=employee,
                    document_type="document",
                    file=uploaded_file,
                    original_file_name=getattr(
                        uploaded_file,
                        "name",
                        "",
                    ),
                )

        return user


    # =========================================================
    # DELETE USER
    # =========================================================

    @staticmethod
    @transaction.atomic
    def delete_user(user, deleted_by=None):

        user.is_active = False
        user.is_deleted = True
        user.updated_by = deleted_by

        user.save(
            update_fields=[
                "is_active",
                "is_deleted",
                "updated_by",
            ]
        )

        if user.employee:
            user.employee.status = "inactive"

            user.employee.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

        return user
