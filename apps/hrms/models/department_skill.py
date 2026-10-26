import uuid

from django.db import models

from apps.masters.models.company import Company
from apps.masters.models.plant import Plant
from apps.masters.models.department import Department

from apps.hrms.models.skill import Skill


class DepartmentSkill(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="department_skills"
    )

    plant = models.ForeignKey(
        Plant,
        on_delete=models.CASCADE,
        related_name="department_skills"
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="department_skills"
    )

    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name="department_requirements"
    )

    # Required proficiency
    required_level = models.PositiveSmallIntegerField(
        default=1
    )

    is_mandatory = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "department_skills"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "department",
                    "skill"
                ],
                name="unique_skill_per_department"
            )
        ]

    def __str__(self):
        return (
            f"{self.department} - "
            f"{self.skill} - "
            f"Level {self.required_level}"
        )