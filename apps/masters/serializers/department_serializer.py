# from rest_framework import serializers

# from apps.masters.models.department import Department
# from apps.masters.models.plant import Plant


# class DepartmentCreateSerializer(serializers.ModelSerializer):

#     plant = serializers.UUIDField(write_only=True)

#     class Meta:
#         model = Department
#         fields = [
#             "plant",
#             "name",
#         ]

#     def validate_plant(self, value):

#         try:
#             return Plant.objects.get(id=value)

#         except Plant.DoesNotExist:
#             raise serializers.ValidationError(
#                 "Plant does not exist."
#             )

#     def validate_name(self, value):

#         value = value.strip()

#         if not value:
#             raise serializers.ValidationError(
#                 "Department name is required."
#             )

#         return value

#     def validate(self, attrs):

#         if Department.objects.filter(
#             plant=attrs["plant"],
#             name__iexact=attrs["name"]
#         ).exists():

#             raise serializers.ValidationError(
#                 {
#                     "name": "Department already exists for this plant."
#                 }
#             )

#         return attrs


# class DepartmentListSerializer(serializers.ModelSerializer):

#     plant_name = serializers.CharField(
#         source="plant.name",
#         read_only=True
#     )

#     company_name = serializers.CharField(
#         source="plant.company.name",
#         read_only=True
#     )

#     class Meta:
#         model = Department
#         fields = [
#             "id",
#             "company_name",
#             "plant_name",
#             "name",
#             "is_active",
#             "created_at",
#             "updated_at",
#         ]


# class DepartmentDetailSerializer(serializers.ModelSerializer):

#     plant_name = serializers.CharField(
#         source="plant.name",
#         read_only=True
#     )

#     company_name = serializers.CharField(
#         source="plant.company.name",
#         read_only=True
#     )

#     class Meta:
#         model = Department
#         fields = [
#             "id",
#             "plant",
#             "plant_name",
#             "company_name",
#             "name",
#             "is_active",
#             "created_at",
#             "updated_at",
#         ]


# class DepartmentUpdateSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Department
#         fields = [
#             "name",
#             "is_active",
#         ]

#     def validate_name(self, value):

#         value = value.strip()

#         if not value:
#             raise serializers.ValidationError(
#                 "Department name is required."
#             )

#         if Department.objects.filter(
#             plant=self.instance.plant,
#             name__iexact=value
#         ).exclude(
#             id=self.instance.id
#         ).exists():

#             raise serializers.ValidationError(
#                 "Department already exists."
#             )

#         return value
from rest_framework import serializers

from apps.masters.models.company import Company
from apps.masters.models.department import Department
from apps.masters.models.plant import Plant


# =============================================================
# CREATE
# =============================================================

class DepartmentCreateSerializer(serializers.ModelSerializer):

    company = serializers.UUIDField(
        write_only=True
    )

    plant = serializers.UUIDField(
        write_only=True
    )

    department_head = serializers.UUIDField(
        required=False,
        allow_null=True,
        write_only=True
    )

    class Meta:
        model = Department

        fields = [
            "company",
            "plant",
            "name",
            "code",
            "description",
            "department_head",
            "is_active",
        ]

    # =========================================================
    # COMPANY
    # =========================================================

    def validate_company(self, value):

        try:

            return Company.objects.get(
                id=value,
                is_active=True
            )

        except Company.DoesNotExist:

            raise serializers.ValidationError(
                "Company does not exist or is inactive."
            )

    # =========================================================
    # PLANT
    # =========================================================

    def validate_plant(self, value):

        try:

            return Plant.objects.select_related(
                "company"
            ).get(
                id=value,
                is_active=True
            )

        except Plant.DoesNotExist:

            raise serializers.ValidationError(
                "Plant does not exist or is inactive."
            )

    # =========================================================
    # NAME
    # =========================================================

    def validate_name(self, value):

        value = value.strip()

        if not value:

            raise serializers.ValidationError(
                "Department name is required."
            )

        return value

    # =========================================================
    # CODE
    # =========================================================

    def validate_code(self, value):

        value = value.strip().upper()

        if not value:

            raise serializers.ValidationError(
                "Department code is required."
            )

        return value

    # =========================================================
    # DESCRIPTION
    # =========================================================

    def validate_description(self, value):

        if value:

            value = value.strip()

        return value

    # =========================================================
    # VALIDATE
    # =========================================================

    def validate(self, attrs):

        company = attrs["company"]
        plant = attrs["plant"]
        name = attrs["name"]
        code = attrs["code"]

        # -----------------------------------------------------
        # PLANT MUST BELONG TO COMPANY
        # -----------------------------------------------------

        if plant.company_id != company.id:

            raise serializers.ValidationError(
                {
                    "plant": [
                        "Selected plant does not belong to "
                        "the selected company."
                    ]
                }
            )

        # -----------------------------------------------------
        # DUPLICATE NAME
        # -----------------------------------------------------

        if Department.objects.filter(
            company=company,
            plant=plant,
            name__iexact=name
        ).exists():

            raise serializers.ValidationError(
                {
                    "name": [
                        "Department already exists for this plant."
                    ]
                }
            )

        # -----------------------------------------------------
        # DUPLICATE CODE
        # -----------------------------------------------------

        if Department.objects.filter(
            company=company,
            plant=plant,
            code__iexact=code
        ).exists():

            raise serializers.ValidationError(
                {
                    "code": [
                        "Department code already exists for this plant."
                    ]
                }
            )

        return attrs

class DepartmentListSerializer(
    serializers.ModelSerializer
):

    company_name = serializers.CharField(
        source="company.name",
        read_only=True
    )

    plant_name = serializers.CharField(
        source="plant.name",
        read_only=True
    )

    department_head_name = serializers.SerializerMethodField()

    class Meta:
        model = Department

        fields = [
            "id",

            "company",
            "company_name",

            "plant",
            "plant_name",

            "name",
            "code",
            "description",

            "department_head",
            "department_head_name",

            "is_active",

            "created_at",
            "updated_at",
        ]

    def get_department_head_name(self, obj):

        if not obj.department_head:
            return None

        return (
            f"{obj.department_head.first_name} "
            f"{obj.department_head.last_name}"
        ).strip()

class DepartmentDetailSerializer(
    DepartmentListSerializer
):
    pass

class DepartmentUpdateSerializer(
    serializers.ModelSerializer
):

    department_head = serializers.UUIDField(
        required=False,
        allow_null=True
    )

    class Meta:
        model = Department

        fields = [
            "name",
            "code",
            "description",
            "department_head",
            "is_active",
        ]

    # =========================================================
    # NAME
    # =========================================================

    def validate_name(self, value):

        value = value.strip()

        if not value:

            raise serializers.ValidationError(
                "Department name is required."
            )

        department = self.instance

        if Department.objects.filter(
            company=department.company,
            plant=department.plant,
            name__iexact=value
        ).exclude(
            id=department.id
        ).exists():

            raise serializers.ValidationError(
                "Department name already exists for this plant."
            )

        return value

    # =========================================================
    # CODE
    # =========================================================

    def validate_code(self, value):

        value = value.strip().upper()

        department = self.instance

        if Department.objects.filter(
            company=department.company,
            plant=department.plant,
            code__iexact=value
        ).exclude(
            id=department.id
        ).exists():

            raise serializers.ValidationError(
                "Department code already exists for this plant."
            )

        return value

    # =========================================================
    # DESCRIPTION
    # =========================================================

    def validate_description(self, value):

        if value:
            value = value.strip()

        return value