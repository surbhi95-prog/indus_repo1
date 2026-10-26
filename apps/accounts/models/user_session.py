# import uuid

# from django.db import models
# from django.conf import settings


# class UserSession(models.Model):

#     id = models.UUIDField(
#         primary_key=True,
#         default=uuid.uuid4,
#         editable=False
#     )

#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE
#     )

#     refresh_token_hash = models.TextField(
#         blank=True,
#         null=True
#     )

#     device_type = models.CharField(
#         max_length=50
#     )

#     device_name = models.CharField(
#         max_length=255
#     )

#     user_agent = models.TextField(
#         blank=True,
#         null=True
#     )

#     ip_address = models.GenericIPAddressField()

#     is_active = models.BooleanField(
#         default=True
#     )

#     expires_at = models.DateTimeField()

#     last_activity = models.DateTimeField(
#         null=True,
#         blank=True
#     )

#     logged_out_at = models.DateTimeField(
#         null=True,
#         blank=True
#     )

#     created_at = models.DateTimeField(
#         auto_now_add=True
#     )

#     class Meta:
#         db_table = "user_sessions"




import uuid

from django.db import models
from django.conf import settings


class UserSession(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sessions"
    )

    refresh_token = models.TextField(
        blank=True,
        null=True
    )

    device_type = models.CharField(
        max_length=50
    )

    device_name = models.CharField(
        max_length=255
    )

    user_agent = models.TextField(
        blank=True,
        null=True
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    expires_at = models.DateTimeField()

    last_activity = models.DateTimeField(
        null=True,
        blank=True
    )

    logged_out_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "user_sessions"

    def __str__(self):
        return f"{self.user.email} - {self.id}"

