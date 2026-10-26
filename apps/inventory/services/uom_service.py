# from django.db import IntegrityError, transaction
# from rest_framework.exceptions import ValidationError

# from apps.inventory.models.uom import UOM


# class UOMService:

#     @staticmethod
#     @transaction.atomic
#     def create(data):
#         try:
#             return UOM.objects.create(**data)
#         except IntegrityError:
#             raise ValidationError(
#                 "UOM code already exists for this plant."
#             )

#     @staticmethod
#     @transaction.atomic
#     def update(uom, data):
#         try:
#             for field, value in data.items():
#                 setattr(uom, field, value)

#             uom.save()

#             return uom

#         except IntegrityError:
#             raise ValidationError(
#                 "UOM code already exists for this plant."
#             )

#     @staticmethod
#     def get_by_id(uom_id):
#         try:
#             return UOM.objects.select_related(
#                 "company",
#                 "plant"
#             ).get(id=uom_id)

#         except UOM.DoesNotExist:
#             raise ValidationError(
#                 "UOM not found."
#             )

#     @staticmethod
#     def list(
#         *,
#         company_id=None,
#         plant_id=None,
#         is_active=None
#     ):
#         queryset = UOM.objects.select_related(
#             "company",
#             "plant"
#         )

#         if company_id:
#             queryset = queryset.filter(
#                 company_id=company_id
#             )

#         if plant_id:
#             queryset = queryset.filter(
#                 plant_id=plant_id
#             )

#         if is_active is not None:
#             queryset = queryset.filter(
#                 is_active=is_active
#             )

#         return queryset.order_by("name")

#     @staticmethod
#     @transaction.atomic
#     def activate(uom):
#         uom.is_active = True
#         uom.save(update_fields=["is_active"])

#         return uom

#     @staticmethod
#     @transaction.atomic
#     def deactivate(uom):
#         uom.is_active = False
#         uom.save(update_fields=["is_active"])

#         return uom


from django.db import IntegrityError, transaction
from rest_framework.exceptions import ValidationError

from apps.inventory.models.uom import UOM


class UOMService:

    @staticmethod
    @transaction.atomic
    def create(data):

        try:
            return UOM.objects.create(**data)

        except IntegrityError:
            raise ValidationError(
                "UOM code already exists for this plant."
            )

    @staticmethod
    @transaction.atomic
    def update(uom, data):

        try:

            for field, value in data.items():
                setattr(uom, field, value)

            uom.save()

            return uom

        except IntegrityError:
            raise ValidationError(
                "UOM code already exists for this plant."
            )

    @staticmethod
    def get_by_id(uom_id):

        try:

            return UOM.objects.select_related(
                "company",
                "plant"
            ).get(id=uom_id)

        except UOM.DoesNotExist:
            raise ValidationError(
                "UOM not found."
            )

    @staticmethod
    def list(
        *,
        company_id=None,
        plant_id=None,
        is_active=None
    ):

        queryset = UOM.objects.select_related(
            "company",
            "plant"
        )

        if company_id:
            queryset = queryset.filter(
                company_id=company_id
            )

        if plant_id:
            queryset = queryset.filter(
                plant_id=plant_id
            )

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active
            )

        return queryset.order_by("name")

    @staticmethod
    @transaction.atomic
    def activate(uom):

        uom.is_active = True

        uom.save(
            update_fields=["is_active"]
        )

        return uom

    @staticmethod
    @transaction.atomic
    def deactivate(uom):

        uom.is_active = False

        uom.save(
            update_fields=["is_active"]
        )

        return uom