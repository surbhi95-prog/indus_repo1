from rest_framework import serializers

from apps.hrms.models.roster import Roster, RosterAssignment
from apps.hrms.models.shift import Shift
from apps.hrms.shift_types import normalize_shift_type


class RosterSerializer(serializers.ModelSerializer):
    company_id = serializers.PrimaryKeyRelatedField(source="company", queryset=Roster._meta.get_field("company").remote_field.model.objects.all())
    plant_id = serializers.PrimaryKeyRelatedField(source="plant", queryset=Roster._meta.get_field("plant").remote_field.model.objects.all())
    department_id = serializers.PrimaryKeyRelatedField(source="department", queryset=Roster._meta.get_field("department").remote_field.model.objects.all(), required=False, allow_null=True)
    total_employees = serializers.IntegerField(read_only=True)

    class Meta:
        model = Roster
        fields = ("id", "name", "company_id", "plant_id", "department_id", "start_date", "end_date", "status", "total_employees", "created_at", "updated_at", "created_by_name", "updated_by_name")
        read_only_fields = ("id", "created_at", "updated_at", "created_by_name", "updated_by_name")
        extra_kwargs = {"status": {"required": False}}

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Name cannot be blank.")
        return value

    def validate_status(self, value):
        normalized = value.strip().upper()
        if normalized not in dict(Roster.STATUS_CHOICES):
            raise serializers.ValidationError("Status must be ACTIVE or INACTIVE.")
        return normalized

    def validate(self, attrs):
        company = attrs.get("company", getattr(self.instance, "company", None))
        plant = attrs.get("plant", getattr(self.instance, "plant", None))
        department = attrs.get("department", getattr(self.instance, "department", None))
        start_date = attrs.get("start_date", getattr(self.instance, "start_date", None))
        end_date = attrs.get("end_date", getattr(self.instance, "end_date", None))

        if company and plant and plant.company_id != company.id:
            raise serializers.ValidationError({"plant_id": "The selected plant does not belong to the selected company."})
        if department and (department.company_id != company.id or department.plant_id != plant.id):
            raise serializers.ValidationError({"department_id": "The selected department does not belong to the selected company and plant."})
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError({"end_date": "end_date must be on or after start_date."})
        name = attrs.get("name", getattr(self.instance, "name", None))
        if company and plant and name and start_date and end_date:
            duplicate = Roster.objects.filter(company=company, plant=plant, name=name, start_date=start_date, end_date=end_date, is_deleted=False)
            if self.instance:
                duplicate = duplicate.exclude(pk=self.instance.pk)
            if duplicate.exists():
                raise serializers.ValidationError({"name": "An active roster with this name and date range already exists for the selected plant."})
        if self.instance and start_date and end_date:
            outside = self.instance.assignments.filter(is_deleted=False).exclude(assignment_date__range=(start_date, end_date)).exists()
            if outside:
                raise serializers.ValidationError({"start_date": "Roster dates cannot exclude dates with active assignments."})
        return attrs


class RosterEditSerializer(RosterSerializer):
    class Meta(RosterSerializer.Meta):
        fields = ("name", "department_id", "start_date", "end_date", "status")


class RosterAssignmentUpdateSerializer(serializers.ModelSerializer):
    shift_id = serializers.PrimaryKeyRelatedField(source="shift", queryset=RosterAssignment._meta.get_field("shift").remote_field.model.objects.filter(is_deleted=False, is_active=True), required=False, allow_null=True)
    shift_type = serializers.CharField(write_only=True, required=False)
    day_type = serializers.ChoiceField(choices=RosterAssignment.DAY_TYPE_CHOICES, required=False, allow_null=True)

    class Meta:
        model = RosterAssignment
        fields = ("shift_id", "shift_type", "day_type")

    def validate(self, attrs):
        shift = attrs.get("shift", self.instance.shift)
        day_type = attrs.get("day_type", self.instance.day_type)
        shift_type = attrs.get("shift_type")
        if shift_type:
            shift_type = normalize_shift_type(shift_type)
            if shift_type not in {choice[0] for choice in Shift.SHIFT_TYPE_CHOICES}:
                raise serializers.ValidationError({"shift_type": "Invalid shift_type."})
        if day_type == "WORKING_DAY" and shift is None:
            raise serializers.ValidationError({"shift_id": "A shift is required for a working day."})
        if day_type != "WORKING_DAY" and shift is not None:
            raise serializers.ValidationError({"shift_id": "A shift must be null for a non-working day."})
        if shift:
            roster = self.instance.roster
            if shift.company_id != roster.company_id or shift.plant_id != roster.plant_id:
                raise serializers.ValidationError({"shift_id": "The selected shift does not belong to this roster's company and plant."})
            if shift_type and shift.shift_type.lower() != shift_type.strip().lower():
                raise serializers.ValidationError({"shift_type": "The selected shift does not match shift_type."})
            if not shift_type:
                attrs["shift_type"] = shift.shift_type
        elif shift_type:
            attrs["shift_type"] = shift_type.strip().lower()
        return attrs

    def update(self, instance, validated_data):
        validated_data.pop("shift_type", None)
        validated_data["source"] = "manual"
        return super().update(instance, validated_data)


class RosterAssignmentListSerializer(serializers.ModelSerializer):
    assignment_id = serializers.UUIDField(source="id", read_only=True)
    roster_id = serializers.UUIDField(source="roster.id", read_only=True)
    roster_name = serializers.CharField(source="roster.name", read_only=True)
    roster_start_date = serializers.DateField(source="roster.start_date", read_only=True)
    roster_end_date = serializers.DateField(source="roster.end_date", read_only=True)
    roster_status = serializers.CharField(source="roster.status", read_only=True)
    company_id = serializers.UUIDField(source="roster.company_id", read_only=True)
    company_name = serializers.CharField(source="roster.company.name", read_only=True)
    plant_id = serializers.UUIDField(source="roster.plant_id", read_only=True)
    plant_name = serializers.CharField(source="roster.plant.name", read_only=True, allow_null=True)
    department_id = serializers.UUIDField(source="roster.department_id", read_only=True, allow_null=True)
    employee_id = serializers.UUIDField(read_only=True)
    employee_code = serializers.CharField(source="employee.employee_code", read_only=True)
    employee_name = serializers.SerializerMethodField()
    shift_id = serializers.UUIDField(read_only=True, allow_null=True)
    shift_name = serializers.CharField(source="shift.name", read_only=True, allow_null=True)
    shift_code = serializers.CharField(source="shift.code", read_only=True, allow_null=True)
    shift_time = serializers.SerializerMethodField()
    shift_type = serializers.CharField(source="shift.shift_type", read_only=True, allow_null=True)
    assignment_date = serializers.DateField(read_only=True)

    class Meta:
        model = RosterAssignment
        fields = (
            "assignment_id", "roster_id", "roster_name", "roster_start_date", "roster_end_date",
            "roster_status", "company_id", "company_name",
            "plant_id", "plant_name", "department_id", "employee_id", "employee_code",
            "employee_name", "assignment_date", "shift_id", "shift_name", "shift_code",
            "shift_time", "shift_type", "day_type", "source", "created_at", "updated_at",
            "created_by_name", "updated_by_name",
        )

    def get_employee_name(self, obj):
        return f"{obj.employee.first_name} {obj.employee.last_name}".strip()

    def get_shift_time(self, obj):
        if not obj.shift_id:
            return None
        return f"{obj.shift.start_time.strftime('%H:%M')}-{obj.shift.end_time.strftime('%H:%M')}"
