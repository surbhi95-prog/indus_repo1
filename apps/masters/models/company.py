# import uuid
# from django.db import models


# class Company(models.Model):
    
#     id = models.UUIDField(
#         primary_key=True,
#         default=uuid.uuid4,
#         editable=False
#     )
#     name = models.CharField(
#         max_length=100,
#         unique=True
#     )
#     code = models.CharField(
#         max_length=50,
#         unique=True,
#         blank=True,
#         null=True
#     )
#     is_active = models.BooleanField(
#         default=True
#     )
#     created_at = models.DateTimeField(
#         auto_now_add = True
#     )
#     updated_at = models.DateTimeField(
#         auto_now = True
#         )
#     class Meta:
#         db_table = "companies"
#         ordering = ['name']

#     def __str__(self):
#         return self.name


import uuid

from django.db import models


class Company(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # ---------------------------------------------------------
    # BASIC INFORMATION
    # ---------------------------------------------------------

    name = models.CharField(
        max_length=100,
        unique=True
    )

    code = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True
    )

    legal_name = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    registration_number = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    tax_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    # ---------------------------------------------------------
    # CONTACT INFORMATION
    # ---------------------------------------------------------

    email = models.EmailField(
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )

    website = models.URLField(
        blank=True,
        null=True
    )

    # ---------------------------------------------------------
    # ADDRESS
    # ---------------------------------------------------------

    address_line_1 = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    address_line_2 = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    state = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    country = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    postal_code = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    # ---------------------------------------------------------
    # BRANDING
    # ---------------------------------------------------------

    logo_url = models.URLField(
        blank=True,
        null=True
    )

    # ---------------------------------------------------------
    # REGIONAL SETTINGS
    # ---------------------------------------------------------

    timezone = models.CharField(
        max_length=100,
        default="Asia/Kolkata"
    )

    currency = models.CharField(
        max_length=10,
        default="INR"
    )

    date_format = models.CharField(
        max_length=30,
        default="DD-MM-YYYY"
    )

    # ---------------------------------------------------------
    # STATUS
    # ---------------------------------------------------------

    is_active = models.BooleanField(
        default=True
    )

    # ---------------------------------------------------------
    # TIMESTAMPS
    # ---------------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "companies"
        ordering = ["name"]

    def __str__(self):
        return self.name