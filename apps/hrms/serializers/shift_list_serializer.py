from rest_framework import serializers

from apps.hrms.models.shift import Shift


class ShiftListSerializer(serializers.ModelSerializer):

    # =========================================================
    # RESPONSE FIELD MAPPING
    # =========================================================

    shift_id = serializers.UUIDField(
        source="id",
        read_only=True
    )

    shift_code = serializers.CharField(
        source="code",
        read_only=True
    )

    shift_start_time = serializers.TimeField(
        source="start_time",
        read_only=True
    )

    shift_end_time = serializers.TimeField(
        source="end_time",
        read_only=True
    )

    shift_name = serializers.CharField(
        source="name",
        read_only=True
    )

    shift_company_id = serializers.UUIDField(
        source="company_id",
        read_only=True
    )

    shift_plant_id = serializers.UUIDField(
        source="plant_id",
        read_only=True
    )

    company_name = serializers.CharField(
        source="company.name",
        read_only=True
    )

    plant_name = serializers.CharField(
        source="plant.name",
        read_only=True
    )

    created_by_name = serializers.SerializerMethodField()

    updated_by_name = serializers.SerializerMethodField()

    grace_time = serializers.IntegerField(
        source="grace_minutes",
        read_only=True
    )

    shift_assign_count = serializers.IntegerField(
        read_only=True
    )

    assigned_user_count = serializers.IntegerField(
        read_only=True
    )

    # =========================================================
    # META
    # =========================================================

    class Meta:

        model = Shift

        fields = [

            # -------------------------------------------------
            # Shift identification
            # -------------------------------------------------

            "shift_id",
            "shift_code",
            "shift_name",

            # -------------------------------------------------
            # Shift timing
            # -------------------------------------------------

            "shift_start_time",
            "shift_end_time",

            # -------------------------------------------------
            # Shift type
            # -------------------------------------------------

            "shift_type",

            # -------------------------------------------------
            # Organization
            # -------------------------------------------------

            "shift_company_id",
            "shift_plant_id",
            "company_name",
            "plant_name",

            # -------------------------------------------------
            # Shift settings
            # -------------------------------------------------

            "grace_time",

            # -------------------------------------------------
            # Status
            # -------------------------------------------------

            "is_active",
            "is_deleted",

            # -------------------------------------------------
            # Audit
            # -------------------------------------------------

            "created_at",
            "updated_at",
            "created_by",
            "created_by_name",
            "updated_by",
            "updated_by_name",

            # -------------------------------------------------
            # Assignment count
            # -------------------------------------------------

            "shift_assign_count",
            "assigned_user_count",
        ]

        read_only_fields = fields

    # =========================================================
    # USER NAME HELPER
    # =========================================================

    def _get_user_name(self, user):

        if not user:
            return None

        # -----------------------------------------------------
        # First try User first_name + last_name
        # -----------------------------------------------------

        name = " ".join(
            part.strip()
            for part in [
                getattr(user, "first_name", ""),
                getattr(user, "last_name", ""),
            ]
            if part and str(part).strip()
        ).strip()

        if name:
            return name

        # -----------------------------------------------------
        # Then try Employee first_name + last_name
        # -----------------------------------------------------

        employee = getattr(
            user,
            "employee",
            None
        )

        if employee:

            employee_name = " ".join(
                part.strip()
                for part in [
                    getattr(employee, "first_name", ""),
                    getattr(employee, "last_name", ""),
                ]
                if part and str(part).strip()
            ).strip()

            if employee_name:
                return employee_name

        # -----------------------------------------------------
        # Finally fallback to email
        # -----------------------------------------------------

        return getattr(
            user,
            "email",
            None
        )

    # =========================================================
    # CREATED BY NAME
    # =========================================================

    def get_created_by_name(self, obj):

        return self._get_user_name(
            obj.created_by
        )

    # =========================================================
    # UPDATED BY NAME
    # =========================================================

    def get_updated_by_name(self, obj):

        return self._get_user_name(
            obj.updated_by
        )
