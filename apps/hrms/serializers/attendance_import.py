from rest_framework import serializers

from apps.hrms.models.attendance_import import AttendanceImport
from apps.hrms.models.attendance_import_row import AttendanceImportRow


class AttendanceImportSerializer(serializers.ModelSerializer):

    class Meta:
        model = AttendanceImport

        fields = [
            "id",
            "company",
            "plant",
            "month",
            "year",
            "file_name",
            "file",
            "uploaded_by",
            "total_rows",
            "successful_rows",
            "failed_rows",
            "status",
            "error_message",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "file_name",
            "uploaded_by",
            "total_rows",
            "successful_rows",
            "failed_rows",
            "status",
            "error_message",
            "created_at",
            "updated_at",
        ]

    def validate_file(self, value):

        if not value.name.lower().endswith(
            (".xlsx", ".xls")
        ):
            raise serializers.ValidationError(
                "Only XLSX or XLS files are allowed."
            )

        return value


class AttendanceImportRowSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = AttendanceImportRow

        fields = [
            "id",
            "attendance_import",
            "row_number",
            "employee",
            "employee_code",
            "attendance_date",
            "in_time",
            "out_time",
            "status",
            "error_message",
        ]

        read_only_fields = [
            "id",
            "status",
            "error_message",
        ]