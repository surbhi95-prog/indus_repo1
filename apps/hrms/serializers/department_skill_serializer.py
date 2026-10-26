from rest_framework import serializers

from apps.hrms.models.department_skill import DepartmentSkill


class DepartmentSkillSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = DepartmentSkill

        fields = [
            "id",
            "company",
            "plant",
            "department",
            "skill",
            "is_mandatory",
            "minimum_level",
            "target_level",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):

        minimum_level = attrs.get(
            "minimum_level",
            1
        )

        target_level = attrs.get(
            "target_level",
            3
        )

        if minimum_level > 5:

            raise serializers.ValidationError({
                "minimum_level":
                "Minimum level cannot be greater than 5."
            })

        if target_level > 5:

            raise serializers.ValidationError({
                "target_level":
                "Target level cannot be greater than 5."
            })

        if minimum_level > target_level:

            raise serializers.ValidationError({
                "minimum_level":
                "Minimum level cannot be greater than target level."
            })

        return attrs