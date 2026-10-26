# from django.db import IntegrityError, transaction
# from django.utils import timezone
# from rest_framework.exceptions import ValidationError

# from apps.inventory.models.batch import Batch


# class BatchService:

#     @staticmethod
#     @transaction.atomic
#     def create(data):

#         item = data.get("item")
#         plant = data.get("plant")
#         company = data.get("company")

#         BatchService._validate_item(
#             company=company,
#             plant=plant,
#             item=item
#         )

#         BatchService._validate_dates(data)

#         try:
#             return Batch.objects.create(**data)

#         except IntegrityError:
#             raise ValidationError(
#                 "Batch number already exists for this item and plant."
#             )

#     @staticmethod
#     @transaction.atomic
#     def update(batch, data):

#         item = data.get(
#             "item",
#             batch.item
#         )

#         plant = data.get(
#             "plant",
#             batch.plant
#         )

#         company = data.get(
#             "company",
#             batch.company
#         )

#         BatchService._validate_item(
#             company=company,
#             plant=plant,
#             item=item
#         )

#         BatchService._validate_dates(data, batch)

#         try:

#             for field, value in data.items():
#                 setattr(batch, field, value)

#             batch.save()

#             return batch

#         except IntegrityError:
#             raise ValidationError(
#                 "Batch number already exists for this item and plant."
#             )

#     @staticmethod
#     def _validate_item(
#         *,
#         company,
#         plant,
#         item
#     ):

#         if not company:
#             raise ValidationError(
#                 "Company is required."
#             )

#         if not plant:
#             raise ValidationError(
#                 "Plant is required."
#             )

#         if not item:
#             raise ValidationError(
#                 "Item is required."
#             )

#         if plant.company_id != company.id:
#             raise ValidationError(
#                 "Plant does not belong to selected company."
#             )

#         if item.company_id != company.id:
#             raise ValidationError(
#                 "Item does not belong to selected company."
#             )

#         if item.plant_id != plant.id:
#             raise ValidationError(
#                 "Item does not belong to selected plant."
#             )

#         if not item.is_active:
#             raise ValidationError(
#                 "Item is inactive."
#             )

#     @staticmethod
#     def _validate_dates(data, batch=None):

#         manufacture_date = data.get(
#             "manufacture_date",
#             batch.manufacture_date if batch else None
#         )

#         expiry_date = data.get(
#             "expiry_date",
#             batch.expiry_date if batch else None
#         )

#         if (
#             manufacture_date
#             and expiry_date
#             and expiry_date < manufacture_date
#         ):
#             raise ValidationError(
#                 "Expiry date cannot be before manufacture date."
#             )

#         if expiry_date and expiry_date < timezone.now().date():
#             raise ValidationError(
#                 "Expiry date cannot be in the past."
#             )

#     @staticmethod
#     def get_by_id(batch_id):

#         try:
#             return Batch.objects.select_related(
#                 "company",
#                 "plant",
#                 "item"
#             ).get(id=batch_id)

#         except Batch.DoesNotExist:
#             raise ValidationError(
#                 "Batch not found."
#             )

#     @staticmethod
#     def list(
#         *,
#         company_id=None,
#         plant_id=None,
#         item_id=None,
#         is_active=None
#     ):

#         queryset = Batch.objects.select_related(
#             "company",
#             "plant",
#             "item"
#         )

#         if company_id:
#             queryset = queryset.filter(
#                 company_id=company_id
#             )

#         if plant_id:
#             queryset = queryset.filter(
#                 plant_id=plant_id
#             )

#         if item_id:
#             queryset = queryset.filter(
#                 item_id=item_id
#             )

#         if is_active is not None:
#             queryset = queryset.filter(
#                 is_active=is_active
#             )

#         return queryset.order_by("-created_at")


from django.db import IntegrityError, transaction
from django.db.models import Q
from django.utils import timezone

from rest_framework.exceptions import ValidationError

from apps.inventory.models.batch import Batch


class BatchService:

    @staticmethod
    @transaction.atomic
    def create(data):

        item = data.get("item")
        plant = data.get("plant")
        company = data.get("company")

        BatchService._validate_item(
            company=company,
            plant=plant,
            item=item
        )

        BatchService._validate_dates(data)

        try:

            return Batch.objects.create(
                **data
            )

        except IntegrityError:

            raise ValidationError(
                "Batch number already exists for this item and plant."
            )

    @staticmethod
    @transaction.atomic
    def update(batch, data):

        item = data.get(
            "item",
            batch.item
        )

        plant = data.get(
            "plant",
            batch.plant
        )

        company = data.get(
            "company",
            batch.company
        )

        BatchService._validate_item(
            company=company,
            plant=plant,
            item=item
        )

        BatchService._validate_dates(
            data,
            batch
        )

        try:

            for field, value in data.items():

                setattr(
                    batch,
                    field,
                    value
                )

            batch.save()

            return batch

        except IntegrityError:

            raise ValidationError(
                "Batch number already exists for this item and plant."
            )

    @staticmethod
    def _validate_item(
        *,
        company,
        plant,
        item
    ):

        if not company:
            raise ValidationError(
                "Company is required."
            )

        if not plant:
            raise ValidationError(
                "Plant is required."
            )

        if not item:
            raise ValidationError(
                "Item is required."
            )

        if plant.company_id != company.id:

            raise ValidationError(
                "Plant does not belong to selected company."
            )

        if item.company_id != company.id:

            raise ValidationError(
                "Item does not belong to selected company."
            )

        if item.plant_id != plant.id:

            raise ValidationError(
                "Item does not belong to selected plant."
            )

        if hasattr(item, "is_active") and not item.is_active:

            raise ValidationError(
                "Item is inactive."
            )

    @staticmethod
    def _validate_dates(data, batch=None):

        manufacture_date = data.get(
            "manufacture_date",
            batch.manufacture_date
            if batch else None
        )

        expiry_date = data.get(
            "expiry_date",
            batch.expiry_date
            if batch else None
        )

        if (
            manufacture_date
            and expiry_date
            and expiry_date < manufacture_date
        ):

            raise ValidationError(
                "Expiry date cannot be before manufacture date."
            )

        if (
            expiry_date
            and expiry_date < timezone.now().date()
        ):

            raise ValidationError(
                "Expiry date cannot be in the past."
            )

    @staticmethod
    def get_by_id(batch_id):

        try:

            return (
                Batch.objects
                .select_related(
                    "company",
                    "plant",
                    "item"
                )
                .get(
                    id=batch_id
                )
            )

        except Batch.DoesNotExist:

            raise ValidationError(
                "Batch not found."
            )

    @staticmethod
    def list(
        *,
        company_id=None,
        plant_id=None,
        item_id=None,
        is_active=None,
        expiry_before=None,
        search=None
    ):

        queryset = (
            Batch.objects
            .select_related(
                "company",
                "plant",
                "item"
            )
        )

        if company_id:

            queryset = queryset.filter(
                company_id=company_id
            )

        if plant_id:

            queryset = queryset.filter(
                plant_id=plant_id
            )

        if item_id:

            queryset = queryset.filter(
                item_id=item_id
            )

        if is_active is not None:

            if isinstance(is_active, str):

                is_active = (
                    is_active.lower()
                    in ["true", "1", "yes"]
                )

            queryset = queryset.filter(
                is_active=is_active
            )

        if expiry_before:

            queryset = queryset.filter(
                expiry_date__lte=expiry_before
            )

        if search:

            queryset = queryset.filter(
                Q(batch_number__icontains=search)
            )

        return queryset.order_by(
            "-created_at"
        )