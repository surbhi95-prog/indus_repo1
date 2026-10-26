import uuid

from django.db import models

from apps.masters.models.company import Company
from apps.masters.models.plant import Plant


class Skill(models.Model):

    SKILL_TYPE_CHOICES = (
        ("technical", "Technical"),
        ("functional", "Functional"),
        ("behavioral", "Behavioral"),
        ("safety", "Safety"),
        ("quality", "Quality"),
        ("soft_skill", "Soft Skill"),
        ("machine", "Machine"),
        ("other", "Other"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="skills"
    )

    plant = models.ForeignKey(
        Plant,
        on_delete=models.CASCADE,
        related_name="skills"
    )

    name = models.CharField(
        max_length=150
    )

    code = models.CharField(
        max_length=50
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    skill_type = models.CharField(
        max_length=30,
        choices=SKILL_TYPE_CHOICES,
        default="technical"
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
        db_table = "skills"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "plant",
                    "code"
                ],
                name="unique_skill_code_per_plant"
            ),
            models.UniqueConstraint(
                fields=[
                    "plant",
                    "name"
                ],
                name="unique_skill_name_per_plant"
            ),
        ]

        ordering = ["name"]

    def __str__(self):
        return f"{self.code} - {self.name}"