from rest_framework import serializers

from apps.hrms.models.shift import Shift
from apps.hrms.shift_types import normalize_shift_type
from apps.masters.models.company import Company
from apps.masters.models.plant import Plant


class ShiftSerializer(serializers.ModelSerializer):

    shift_type = serializers.CharField(max_length=20)

    # =========================================================
    # COMPANY
    # =========================================================

    company_id = serializers.PrimaryKeyRelatedField(
        source="company",
        queryset=Company.objects.all(),
        write_only=True
    )

    # =========================================================
    # PLANT
    # =========================================================

    plant_id = serializers.PrimaryKeyRelatedField(
        source="plant",
        queryset=Plant.objects.all(),
        write_only=True
    )

    # =========================================================
    # SHIFT NAME
    # =========================================================

    shift_name = serializers.CharField(
        source="name"
    )

    # =========================================================
    # SHIFT CODE
    #
    # Backend generated.
    # Frontend should NOT send this field.
    # It is returned only in the response.
    # =========================================================

    shift_code = serializers.CharField(
        source="code",
        read_only=True
    )

    # =========================================================
    # GRACE TIME
    # =========================================================

    shift_grace_time = serializers.IntegerField(
        source="grace_minutes"
    )

    # =========================================================
    # META
    # =========================================================

    class Meta:

        model = Shift

        fields = [
            "id",

            "company_id",
            "plant_id",

            "shift_name",
            "shift_code",

            "shift_type",

            "start_time",
            "end_time",

            "shift_grace_time",

            "is_active",
            "is_deleted",

            "created_by",
            "updated_by",

            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",

            "shift_code",

            "is_deleted",

            "created_by",
            "updated_by",

            "created_at",
            "updated_at",
        ]

    # =========================================================
    # VALIDATION
    # =========================================================

    def validate(self, attrs):

        # -----------------------------------------------------
        # COMPANY
        # -----------------------------------------------------

        company = attrs.get("company")

        if not company:

            raise serializers.ValidationError({
                "company_id":
                    "Company is required."
            })

        # -----------------------------------------------------
        # PLANT
        # -----------------------------------------------------

        plant = attrs.get("plant")

        if not plant:

            raise serializers.ValidationError({
                "plant_id":
                    "Plant is required."
            })

        # -----------------------------------------------------
        # COMPANY -> PLANT VALIDATION
        # -----------------------------------------------------

        if plant.company_id != company.id:

            raise serializers.ValidationError({
                "plant_id":
                    "The selected plant does not belong to "
                    "the selected company."
            })

        # -----------------------------------------------------
        # SHIFT NAME
        # -----------------------------------------------------

        name = attrs.get("name")

        if not name or not name.strip():

            raise serializers.ValidationError({
                "shift_name":
                    "Shift name is required."
            })

        attrs["name"] = name.strip()

        # -----------------------------------------------------
        # GRACE TIME
        # -----------------------------------------------------

        grace_minutes = attrs.get(
            "grace_minutes"
        )

        if (
            grace_minutes is not None
            and grace_minutes < 0
        ):

            raise serializers.ValidationError({
                "shift_grace_time":
                    "Grace time cannot be negative."
            })

        return attrs

    # =========================================================
    # SHIFT TYPE VALIDATION
    # =========================================================

    def validate_shift_type(self, value):

        value = normalize_shift_type(value)
        valid_types = {choice[0] for choice in Shift.SHIFT_TYPE_CHOICES}

        if value not in valid_types:

            raise serializers.ValidationError(
                "Shift type must be General or Contract."
            )

        return value
