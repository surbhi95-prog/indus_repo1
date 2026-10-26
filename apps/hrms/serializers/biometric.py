from rest_framework import serializers

from apps.hrms.models.biometric_device import BiometricDevice
from apps.hrms.models.biometric_employee import BiometricEmployee
from apps.hrms.models.biometric_punch import BiometricPunch


class BiometricDeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = BiometricDevice

        fields = [
            "id",
            "company",
            "plant",
            "name",
            "device_code",
            "device_type",
            "ip_address",
            "port",
            "serial_number",
            "location",
            "is_active",
            "last_sync_at",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "last_sync_at",
            "created_at",
            "updated_at",
        ]


class BiometricEmployeeSerializer(serializers.ModelSerializer):

    employee_code = serializers.CharField(
        source="employee.employee_code",
        read_only=True
    )

    class Meta:
        model = BiometricEmployee

        fields = [
            "id",
            "employee",
            "employee_code",
            "device",
            "biometric_user_id",
            "card_number",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class BiometricPunchSerializer(serializers.ModelSerializer):

    class Meta:
        model = BiometricPunch

        fields = [
            "id",
            "device",
            "employee",
            "biometric_user_id",
            "punch_datetime",
            "punch_type",
            "raw_data",
            "sync_status",
            "error_message",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "employee",
            "sync_status",
            "error_message",
            "created_at",
        ]