from rest_framework import serializers

from apps.hrms.models.employee_skill import EmployeeSkill


class EmployeeSkillSerializer(
    serializers.ModelSerializer
):

    employee_name = serializers.SerializerMethodField()

    skill_name = serializers.CharField(
        source="skill.name",
        read_only=True
    )

    skill_code = serializers.CharField(
        source="skill.code",
        read_only=True
    )

    level_name = serializers.CharField(
        source="get_level_display",
        read_only=True
    )

    class Meta:

        model = EmployeeSkill

        fields = [
            "id",
            "employee",
            "employee_name",
            "skill",
            "skill_name",
            "skill_code",
            "level",
            "level_name",
            "assessed_by",
            "assessed_at",
            "remarks",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "employee_name",
            "skill_name",
            "skill_code",
            "level_name",
            "created_at",
            "updated_at",
        ]

    def get_employee_name(self, obj):

        return (
            f"{obj.employee.first_name} "
            f"{obj.employee.last_name}"
        ).strip()