# import uuid

# from django.db import models
# from django.contrib.auth.models import (
#     AbstractBaseUser,
#     PermissionsMixin
# )

# from apps.accounts.models.managers import UserManager


# class User(AbstractBaseUser, PermissionsMixin):

#     id = models.UUIDField(
#         primary_key=True,
#         default=uuid.uuid4,
#         editable=False
#     )

#     company = models.ForeignKey(
#         "masters.Company",
#         on_delete=models.PROTECT,
#         related_name="users",
#         null=True,
#         blank=True
#     )

#     plant = models.ForeignKey(
#         "masters.Plant",
#         on_delete=models.PROTECT,
#         related_name="users",
#         null=True,
#         blank=True
#     )

#     department = models.ForeignKey(
#         "masters.Department",
#         on_delete=models.PROTECT,
#         related_name="users",
#         null=True,
#         blank=True
#     )

#     email = models.EmailField(
#         unique=True,
#         db_index=True
#     )

#     first_name = models.CharField(
#         max_length=100
#     )

#     last_name = models.CharField(
#         max_length=100,
#         blank=True
#     )

#     is_active = models.BooleanField(
#         default=True
#     )

#     is_staff = models.BooleanField(
#         default=False
#     )

#     is_superuser = models.BooleanField(
#         default=False
#     )

#     last_login = models.DateTimeField(
#         null=True,
#         blank=True
#     )

#     created_at = models.DateTimeField(
#         auto_now_add=True
#     )

#     updated_at = models.DateTimeField(
#         auto_now=True
#     )

#     USERNAME_FIELD = "email"

#     REQUIRED_FIELDS = []

#     objects = UserManager()

#     class Meta:
#         db_table = "users"
#         ordering = ["first_name"]

#     def __str__(self):
#         return self.email

#     @property
#     def full_name(self):
#         return f"{self.first_name} {self.last_name}".strip()



# apps/accounts/models/user.py
import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from apps.masters.models.company import Company
from apps.masters.models.plant import Plant
from apps.masters.models.department import Department
from apps.hrms.models.employee import Employee

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # --------------------------------------------------
    # Organization
    # --------------------------------------------------

    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users"
    )

    plant = models.ForeignKey(
        Plant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users"
    )
    encrypted_password = models.TextField(
        null=True,
        blank=True
)
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users"
    )
    SCOPE_CHOICES = (
        ("company", "Company"),
        ("plant", "Plant"),
        ("department", "Department"),
    )

    scope = models.CharField(
        max_length=20,
        choices=SCOPE_CHOICES,
        default="plant",
    )
        # --------------------------------------------------
    # AUDIT / SOFT DELETE
    # --------------------------------------------------

    created_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users_created",
    )

    updated_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users_updated",
    )

    is_deleted = models.BooleanField(
        default=False
    )
    # ----------------  ----------------------------------
    # HRMS Employee
    # --------------------------------------------------

    employee = models.OneToOneField(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="user"
    )

    # --------------------------------------------------
    # Basic information
    # --------------------------------------------------

    email = models.EmailField(
    unique=True,
    null=True,
    blank=True
)

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100,
        blank=True
    )

    # --------------------------------------------------
    # Status
    # --------------------------------------------------

    is_active = models.BooleanField(
        default=True
    )

    is_staff = models.BooleanField(
        default=False
    )

    # --------------------------------------------------
    # Authentication
    # --------------------------------------------------

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email