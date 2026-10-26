import uuid

from django.db import models

from apps.hrms.models.employee import Employee
from apps.hrms.models.skill import Skill


class EmployeeSkill(models.Model):

    PROFICIENCY_CHOICES = (
        (1, "Beginner"),
        (2, "Basic"),
        (3, "Intermediate"),
        (4, "Advanced"),
        (5, "Expert"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="skills"
    )

    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name="employee_skills"
    )

    current_level = models.PositiveSmallIntegerField(
        choices=PROFICIENCY_CHOICES,
        default=1
    )

    years_of_experience = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        default=0
    )

    is_certified = models.BooleanField(
        default=False
    )

    certification_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    certification_date = models.DateField(
        blank=True,
        null=True
    )

    certification_expiry = models.DateField(
        blank=True,
        null=True
    )

    last_assessed_at = models.DateTimeField(
        blank=True,
        null=True
    )

    assessed_by = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="skill_assessments"
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "employee_skills"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "employee",
                    "skill"
                ],
                name="unique_skill_per_employee"
            )
        ]

    def __str__(self):
        return (
            f"{self.employee.employee_code} - "
            f"{self.skill.name}"
        )