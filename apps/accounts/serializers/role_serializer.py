from rest_framework import serializers

from apps.accounts.models.role import Role
from apps.masters.models.company import Company
from apps.masters.models.plant import Plant
from apps.masters.models.department import Department


# class RoleCreateSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Role
#         fields = [
#             "company",
#             "plant",
#             "department",
#             "name",
#             "code",
#             "description",
#         ]

#     def validate(self, attrs):

#         company = attrs.get("company")
#         plant = attrs.get("plant")
#         department = attrs.get("department")

#         # Company is mandatory
#         if not company:
#             raise serializers.ValidationError(
#                 {
#                     "company": "Company is required."
#                 }
#             )

#         # Plant must belong to Company
#         if plant:

#             if plant.company_id != company.id:

#                 raise serializers.ValidationError(
#                     {
#                         "plant": "Plant does not belong to selected company."
#                     }
#                 )

#         # Department must belong to Plant
#         if department:

#             if not plant:

#                 raise serializers.ValidationError(
#                     {
#                         "plant": "Plant is required when department is selected."
#                     }
#                 )

#             if department.plant_id != plant.id:

#                 raise serializers.ValidationError(
#                     {
#                         "department": "Department does not belong to selected plant."
#                     }
#                 )

#         return attrs

#     def validate_name(self, value):

#         return value.strip()

#     def validate_code(self, value):

#         return value.strip().upper()

#     def validate(self, attrs):

#         attrs = super().validate(attrs)

#         company = attrs.get("company")
#         plant = attrs.get("plant")
#         department = attrs.get("department")
#         name = attrs.get("name")
#         code = attrs.get("code")

#         if Role.objects.filter(
#             company=company,
#             plant=plant,
#             department=department,
#             name__iexact=name
#         ).exists():

#             raise serializers.ValidationError(
#                 "Role already exists."
#             )

#         if Role.objects.filter(
#             company=company,
#             plant=plant,
#             department=department,
#             code__iexact=code
#         ).exists():

#             raise serializers.ValidationError(
#                 "Role code already exists."
#             )

#         return attrs







# class RoleCreateSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Role

#         fields = [
#             "company",
#             "plant",
#             # "department",
#             "scope",
#             "name",
#             "code",
#             "description",
#         ]

#         # IMPORTANT
#         # Disable DRF automatic UniqueTogetherValidator.
#         # We will handle uniqueness ourselves.
#         validators = []

#     # =========================================================
#     # VALIDATE
#     # =========================================================

#     def validate(self, attrs):

#         company = attrs.get("company")
#         plant = attrs.get("plant")
#         # department = attrs.get("department")
#         scope = attrs.get("scope")
#         # Department scope is disabled for Role creation.
#         department = None
#         # -----------------------------------------------------
#         # COMPANY
#         # -----------------------------------------------------

#         if not company:

#             raise serializers.ValidationError({
#                 "company": "Company is required."
#             })

#         # -----------------------------------------------------
#         # LEVEL REQUIRED
#         # -----------------------------------------------------

#         if not scope:

#             raise serializers.ValidationError({
#                 "scope": "Role scope is required."
#             })

#         # =====================================================
#         # COMPANY LEVEL
#         # =====================================================

#         if scope == "company":

#             if plant:

#                 raise serializers.ValidationError({
#                     "plant":
#                     "Company-level role cannot have plant."
#                 })

#             if department:

#                 raise serializers.ValidationError({
#                     "department":
#                     "Company-level role cannot have department."
#                 })

#         # =====================================================
#         # PLANT LEVEL
#         # =====================================================

#         elif scope == "plant":

#             if not plant:

#                 raise serializers.ValidationError({
#                     "plant":
#                     "Plant is required for plant-level role."
#                 })

#             # Plant must belong to company

#             if plant.company_id != company.id:

#                 raise serializers.ValidationError({
#                     "plant":
#                     "Selected plant does not belong to selected company."
#                 })

#             # Plant role cannot have department

#             if department:

#                 raise serializers.ValidationError({
#                     "department":
#                     "Plant-level role cannot have department."
#                 })

#         # =====================================================
#         # DEPARTMENT LEVEL
#         # =====================================================

#         # elif scope == "department":

#         #     if not plant:

#         #         raise serializers.ValidationError({
#         #             "plant":
#         #             "Plant is required for department-level role."
#         #         })

#         #     if not department:

#         #         raise serializers.ValidationError({
#         #             "department":
#         #             "Department is required for department-level role."
#         #         })

#         #     # Plant must belong to company

#         #     if plant.company_id != company.id:

#         #         raise serializers.ValidationError({
#         #             "plant":
#         #             "Selected plant does not belong to selected company."
#         #         })

#         #     # Department must belong to plant

#         #     if department.plant_id != plant.id:

#         #         raise serializers.ValidationError({
#         #             "department":
#         #             "Selected department does not belong to selected plant."
#         #         })

#         else:

#             raise serializers.ValidationError({
#                 "scope":
#                 "Invalid role scope."
#             })

#         # =====================================================
#         # CODE UNIQUENESS
#         # =====================================================

#         code = attrs.get("code")

#         if code:

#             code = code.strip().upper()

#             existing_role = Role.objects.filter(
#                 company=company,
#                 plant=plant,
#                 department=department,
#                 code__iexact=code,
#             ).first()

#             if existing_role:

#                 raise serializers.ValidationError({
#                     "code":
#                     "This role code already exists for the selected scope."
#                 })

#         return attrs

#     # =========================================================
#     # NAME
#     # =========================================================

#     def validate_name(self, value):

#         value = value.strip()

#         if not value:

#             raise serializers.ValidationError(
#                 "Role name is required."
#             )

#         return value

#     # =========================================================
#     # CODE
#     # =========================================================

#     def validate_code(self, value):

#         value = value.strip().upper()

#         if not value:

#             raise serializers.ValidationError(
#                 "Role code is required."
#             )

#         return value


    
# # class RoleListSerializer(serializers.ModelSerializer):
# #     """
# #     Serializer for listing roles.
# #     """

# #     company_id = serializers.UUIDField(
# #         source="company.id",
# #         read_only=True
# #     )

# #     company_name = serializers.CharField(
# #         source="company.name",
# #         read_only=True
# #     )

# #     plant_id = serializers.UUIDField(
# #         source="plant.id",
# #         read_only=True
# #     )

# #     plant_name = serializers.CharField(
# #         source="plant.name",
# #         read_only=True
# #     )

# #     department_id = serializers.UUIDField(
# #         source="department.id",
# #         read_only=True
# #     )

# #     department_name = serializers.CharField(
# #         source="department.name",
# #         read_only=True
# #     )

# #     class Meta:
# #         model = Role
# #         fields = [
# #             "id",

# #             "company_id",
# #             "company_name",

# #             "plant_id",
# #             "plant_name",

# #             "department_id",
# #             "department_name",

# #             "name",
# #             "code",
# #             "description",

# #             "is_active",

# #             "created_at",
# #             "updated_at",
# #         ]
class RoleCreateSerializer(serializers.ModelSerializer):

    # ---------------------------------------------------------
    # DEPARTMENT
    # ---------------------------------------------------------
    # We accept this field only so that we can explicitly
    # reject it during validation.
    #
    # It must NEVER be saved for company/plant roles.
    # ---------------------------------------------------------

    department = serializers.UUIDField(
        required=False,
        allow_null=True,
        write_only=True
    )

    class Meta:

        model = Role

        fields = [
            "company",
            "plant",
            "department",
            "scope",
            "name",
            "code",
            "description",
        ]

        # Disable DRF automatic unique validation.
        # We handle it manually below.
        validators = []

    # =========================================================
    # VALIDATE
    # =========================================================

    def validate(self, attrs):

        company = attrs.get(
            "company"
        )

        plant = attrs.get(
            "plant"
        )

        department = attrs.get(
            "department"
        )

        scope = attrs.get(
            "scope"
        )

        # -----------------------------------------------------
        # COMPANY
        # -----------------------------------------------------

        if not company:

            raise serializers.ValidationError({
                "company":
                    "Company is required."
            })

        # -----------------------------------------------------
        # SCOPE
        # -----------------------------------------------------

        if not scope:

            raise serializers.ValidationError({
                "scope":
                    "Role scope is required."
            })

        # Normalize scope
        scope = scope.strip().lower()

        attrs["scope"] = scope

        # =====================================================
        # COMPANY LEVEL
        # =====================================================

        if scope == "company":

            # Company-level role cannot have plant
            if plant:

                raise serializers.ValidationError({
                    "plant":
                        "Company-level role cannot have plant."
                })

            # Company-level role cannot have department
            if department:

                raise serializers.ValidationError({
                    "department":
                        "Department cannot be assigned to a company-level role."
                })

        # =====================================================
        # PLANT LEVEL
        # =====================================================

        elif scope == "plant":

            # Plant is mandatory
            if not plant:

                raise serializers.ValidationError({
                    "plant":
                        "Plant is required for plant-level role."
                })

            # -------------------------------------------------
            # PLANT MUST BELONG TO COMPANY
            # -------------------------------------------------

            if plant.company_id != company.id:

                raise serializers.ValidationError({
                    "plant":
                        "Selected plant does not belong to selected company."
                })

            # -------------------------------------------------
            # DEPARTMENT NOT ALLOWED
            # -------------------------------------------------

            if department:

                raise serializers.ValidationError({
                    "department":
                        "Department cannot be assigned to a plant-level role."
                })

        # =====================================================
        # INVALID SCOPE
        # =====================================================

        else:

            raise serializers.ValidationError({
                "scope":
                    "Invalid role scope."
            })

        # -----------------------------------------------------
        # FORCE DEPARTMENT TO NONE
        # -----------------------------------------------------

        attrs["department"] = None

        # =====================================================
        # CODE UNIQUENESS
        # =====================================================

        code = attrs.get(
            "code"
        )

        if code:

            code = code.strip().upper()

            existing_role = Role.objects.filter(
                company=company,
                plant=plant,
                department=None,
                code__iexact=code,
            ).first()

            if existing_role:

                raise serializers.ValidationError({
                    "code":
                        "This role code already exists for the selected scope."
                })

        return attrs

    # =========================================================
    # NAME
    # =========================================================

    def validate_name(self, value):

        value = value.strip()

        if not value:

            raise serializers.ValidationError(
                "Role name is required."
            )

        return value

    # =========================================================
    # CODE
    # =========================================================

    def validate_code(self, value):

        value = value.strip().upper()

        if not value:

            raise serializers.ValidationError(
                "Role code is required."
            )

        return value

class RoleListSerializer(
    serializers.ModelSerializer
):

    company_id = serializers.UUIDField(
        source="company.id",
        read_only=True
    )

    company_name = serializers.CharField(
        source="company.name",
        read_only=True
    )

    plant_id = serializers.UUIDField(
        source="plant.id",
        read_only=True
    )

    plant_name = serializers.CharField(
        source="plant.name",
        read_only=True
    )

    department_id = serializers.UUIDField(
        source="department.id",
        read_only=True
    )

    department_name = serializers.CharField(
        source="department.name",
        read_only=True
    )

    class Meta:

        model = Role

        fields = [
            "id",

            "company_id",
            "company_name",

            "plant_id",
            "plant_name",

            "department_id",
            "department_name",

            "scope",

            "name",
            "code",
            "description",

            "is_active",

            "created_at",
            # "updated_at",
        ]


class RoleUpdateSerializer(serializers.ModelSerializer):

    company = serializers.UUIDField(required=False)
    plant = serializers.UUIDField(required=False)
    department = serializers.UUIDField(required=False)

    class Meta:
        model = Role
        fields = [
            "company",
            "plant",
            "department",
            "name",
            "code",
            "description",
            "is_active",
        ]

    def validate(self, attrs):

        company_id = attrs.get(
            "company",
            self.instance.company.id if self.instance.company else None
        )

        plant_id = attrs.get(
            "plant",
            self.instance.plant.id if self.instance.plant else None
        )

        department_id = attrs.get(
            "department",
            self.instance.department.id if self.instance.department else None
        )

        company = None
        plant = None
        department = None

        # ---------------- Company ----------------

        if company_id:

            try:
                company = Company.objects.get(
                    id=company_id
                )

            except Company.DoesNotExist:
                raise serializers.ValidationError(
                    {
                        "company": "Company not found."
                    }
                )

            attrs["company"] = company

        # ---------------- Plant ----------------

        if plant_id:

            if company is None:
                raise serializers.ValidationError(
                    {
                        "company": "Company is required."
                    }
                )

            try:
                plant = Plant.objects.get(
                    id=plant_id,
                    company=company
                )

            except Plant.DoesNotExist:
                raise serializers.ValidationError(
                    {
                        "plant": "Plant does not belong to selected company."
                    }
                )

            attrs["plant"] = plant

        # ---------------- Department ----------------

        if department_id:

            if plant is None:
                raise serializers.ValidationError(
                    {
                        "plant": "Plant is required."
                    }
                )

            try:
                department = Department.objects.get(
                    id=department_id,
                    plant=plant
                )

            except Department.DoesNotExist:
                raise serializers.ValidationError(
                    {
                        "department": "Department does not belong to selected plant."
                    }
                )

            attrs["department"] = department

        return attrs

    def validate_name(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Role name is required."
            )

        if Role.objects.filter(
            company=self.instance.company,
            plant=self.instance.plant,
            department=self.instance.department,
            name__iexact=value
        ).exclude(
            id=self.instance.id
        ).exists():

            raise serializers.ValidationError(
                "Role name already exists."
            )

        return value

    def validate_code(self, value):

        value = value.strip().upper()

        if not value:
            raise serializers.ValidationError(
                "Role code is required."
            )

        if Role.objects.filter(
            company=self.instance.company,
            plant=self.instance.plant,
            department=self.instance.department,
            code__iexact=value
        ).exclude(
            id=self.instance.id
        ).exists():

            raise serializers.ValidationError(
                "Role code already exists."
            )

        return value