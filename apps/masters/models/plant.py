# import uuid

# from django.db import models

# from .company import Company


# class Plant(models.Model):
#      id = models.UUIDField(
#           primary_key=True,
#          default=uuid.uuid4,
#          editable=False

#      ) 
#      company = models.ForeignKey(
#           Company,
#           on_delete=models.PROTECT,
#           related_name="plants"
#      )
#      name = models.CharField(
#       max_length=255,
#       unique=True
#      )
#      location = models.CharField(
#           max_length=100,
#           blank=True,
#           null=True
#      )
#      is_active = models.BooleanField(
#           default=True
#      )
#      created_at = models.DateTimeField(
#             auto_now_add=True
#      )
#      updated_at = models.DateTimeField(
#              auto_now = True
#      )

#      class Meta:
#           db_table = "plants"
#           ordering = ['name']

#           constraints = [
#                models.UniqueConstraint(
#                     fields = ["company","name"],
#                     name = "unique_plant_name_per_company"
#                )
#           ]
    
# def __str__(self):
#          return self.name
import uuid

from django.db import models

from .company import Company


class Plant(models.Model):

    # =========================================================
    # BASIC
    # =========================================================

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name="plants"
    )

    name = models.CharField(
        max_length=255,
        null=True,
        blank=True
        
    )

    code = models.CharField(
    max_length=50,
    unique=True,
    null=True,
    blank=True
)

    plant_type = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    # =========================================================
    # ADDRESS
    # =========================================================

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

    # =========================================================
    # CONTACT
    # =========================================================

    email = models.EmailField(
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )

    # =========================================================
    # SETTINGS
    # =========================================================

    timezone = models.CharField(
        max_length=100,
        default="Asia/Kolkata"
    )

    is_active = models.BooleanField(
        default=True
    )

    # =========================================================
    # TIMESTAMPS
    # =========================================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "plants"
        ordering = ["name"]

        constraints = [
            models.UniqueConstraint(
                fields=["company", "name"],
                name="unique_plant_name_per_company"
            ),
            models.UniqueConstraint(
                fields=["company", "code"],
                name="unique_plant_code_per_company"
            ),
        ]

    def __str__(self):
        return self.name