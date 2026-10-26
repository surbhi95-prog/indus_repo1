from rest_framework import serializers

from apps.hrms.models.shift import Shift
from apps.hrms.shift_types import normalize_shift_type


class ShiftUpdateSerializer(serializers.Serializer):
    """Editable fields for shift updates; organization and audit fields stay fixed."""

    shift_name = serializers.CharField(source="name", max_length=100, required=True, allow_blank=False, trim_whitespace=True)
    shift_type = serializers.CharField(max_length=20, required=True)
    start_time = serializers.TimeField(required=True)
    end_time = serializers.TimeField(required=True)
    shift_grace_time = serializers.IntegerField(source="grace_minutes", required=True, min_value=0)
    is_active = serializers.BooleanField(required=True)

    def validate_shift_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Shift name is required.")
        return value

    def validate_shift_type(self, value):
        value = normalize_shift_type(value)
        if value not in {choice[0] for choice in Shift.SHIFT_TYPE_CHOICES}:
            raise serializers.ValidationError("Shift type must be General or Contract.")
        return value

    def to_representation(self, instance):
        from apps.hrms.serializers.shift_serializer import ShiftSerializer
        return ShiftSerializer(instance).data
