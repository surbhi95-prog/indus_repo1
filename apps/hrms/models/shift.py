import uuid

from django.conf import settings
from django.db import models

from apps.masters.models.company import Company
from apps.masters.models.plant import Plant


class Shift(models.Model):

    SHIFT_TYPE_CHOICES = (
        ("general", "General"),
        ("contract", "Contract"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # =========================================================
    # ORGANIZATION
    # =========================================================

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="hrms_shifts"
    )

    plant = models.ForeignKey(
        Plant,
        on_delete=models.CASCADE,
        related_name="hrms_shifts"
    )

    # =========================================================
    # SHIFT INFORMATION
    # =========================================================

    name = models.CharField(
        max_length=100
    )

    code = models.CharField(
        max_length=50
    )

    shift_type = models.CharField(
        max_length=20,
        choices=SHIFT_TYPE_CHOICES
    )

    start_time = models.TimeField()

    end_time = models.TimeField()

    grace_minutes = models.PositiveIntegerField(
        default=15
    )

    # =========================================================
    # EXISTING ATTENDANCE SUPPORT
    # =========================================================

    break_minutes = models.PositiveIntegerField(
        default=60
    )

    minimum_work_minutes = models.PositiveIntegerField(
        default=480
    )

    overtime_after_minutes = models.PositiveIntegerField(
        default=480
    )

    is_overnight = models.BooleanField(
        default=False
    )

    # =========================================================
    # STATUS
    # =========================================================

    is_active = models.BooleanField(
        default=True
    )

    is_deleted = models.BooleanField(
        default=False
    )

    # =========================================================
    # AUDIT
    # =========================================================

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_shifts"
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_shifts"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # =========================================================
    # META
    # =========================================================

    class Meta:

        db_table = "hrms_shifts"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "plant",
                    "code"
                ],
                name="unique_shift_code_per_plant"
            ),
            # -------------------------------------------------
            # SAME SHIFT NAME + SHIFT TYPE
            # -------------------------------------------------
            # Prevent duplicate active shifts having the same:
            # company + plant + name + shift_type
            # -------------------------------------------------
            models.UniqueConstraint(
                fields=[
                    "company",
                    "plant",
                    "name",
                    "shift_type",
                ],
                condition=models.Q(
                    is_deleted=False
                ),
                name="unique_active_shift_name_type",
            ),

            # -------------------------------------------------
            # SAME SHIFT TIME
            # -------------------------------------------------
            # Prevent duplicate active shifts having the same:
            # company + plant + start_time + end_time
            # -------------------------------------------------
            models.UniqueConstraint(
                fields=[
                    "company",
                    "plant",
                    "start_time",
                    "end_time",
                ],
                condition=models.Q(
                    is_deleted=False
                ),
                name="unique_active_shift_time",
            ),
        
        ]

        indexes = [
            models.Index(
                fields=[
                    "company",
                    "plant"
                ]
            ),
            models.Index(
                fields=[
                    "is_active"
                ]
            ),
            models.Index(
                fields=[
                    "is_deleted"
                ]
            ),
        ]

    def __str__(self):

        return f"{self.code} - {self.name}"
