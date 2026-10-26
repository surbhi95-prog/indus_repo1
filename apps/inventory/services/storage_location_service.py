# from django.db import IntegrityError, transaction
# from rest_framework.exceptions import ValidationError

# from apps.inventory.models.storage_location import StorageLocation


# class StorageLocationService:

#     @staticmethod
#     @transaction.atomic
#     def create(data):

#         warehouse = data.get("warehouse")
#         plant = data.get("plant")
#         company = data.get("company")

#         StorageLocationService._validate_relations(
#             company=company,
#             plant=plant,
#             warehouse=warehouse
#         )

#         try:
#             return StorageLocation.objects.create(**data)

#         except IntegrityError:
#             raise ValidationError(
#                 "Storage location code already exists in this warehouse."
#             )

#     @staticmethod
#     @transaction.atomic
#     def update(location, data):

#         company = data.get(
#             "company",
#             location.company
#         )

#         plant = data.get(
#             "plant",
#             location.plant
#         )

#         warehouse = data.get(
#             "warehouse",
#             location.warehouse
#         )

#         StorageLocationService._validate_relations(
#             company=company,
#             plant=plant,
#             warehouse=warehouse
#         )

#         try:

#             for field, value in data.items():
#                 setattr(location, field, value)

#             location.save()

#             return location

#         except IntegrityError:
#             raise ValidationError(
#                 "Storage location code already exists in this warehouse."
#             )

#     @staticmethod
#     def _validate_relations(
#         *,
#         company,
#         plant,
#         warehouse
#     ):

#         if not company:
#             raise ValidationError(
#                 "Company is required."
#             )

#         if not plant:
#             raise ValidationError(
#                 "Plant is required."
#             )

#         if not warehouse:
#             raise ValidationError(
#                 "Warehouse is required."
#             )

#         if plant.company_id != company.id:
#             raise ValidationError(
#                 "Plant does not belong to selected company."
#             )

#         if warehouse.company_id != company.id:
#             raise ValidationError(
#                 "Warehouse does not belong to selected company."
#             )

#         if warehouse.plant_id != plant.id:
#             raise ValidationError(
#                 "Warehouse does not belong to selected plant."
#             )

#         if not warehouse.is_active:
#             raise ValidationError(
#                 "Warehouse is inactive."
#             )

#     @staticmethod
#     def get_by_id(location_id):

#         try:
#             return StorageLocation.objects.select_related(
#                 "company",
#                 "plant",
#                 "warehouse"
#             ).get(id=location_id)

#         except StorageLocation.DoesNotExist:
#             raise ValidationError(
#                 "Storage location not found."
#             )

#     @staticmethod
#     def list(
#         *,
#         company_id=None,
#         plant_id=None,
#         warehouse_id=None,
#         is_active=None
#     ):

#         queryset = StorageLocation.objects.select_related(
#             "company",
#             "plant",
#             "warehouse"
#         )

#         if company_id:
#             queryset = queryset.filter(
#                 company_id=company_id
#             )

#         if plant_id:
#             queryset = queryset.filter(
#                 plant_id=plant_id
#             )

#         if warehouse_id:
#             queryset = queryset.filter(
#                 warehouse_id=warehouse_id
#             )

#         if is_active is not None:
#             queryset = queryset.filter(
#                 is_active=is_active
#             )

#         return queryset.order_by("code")

#     @staticmethod
#     @transaction.atomic
#     def activate(location):

#         location.is_active = True
#         location.save(update_fields=[
#             "is_active",
#             "updated_at"
#         ])

#         return location

#     @staticmethod
#     @transaction.atomic
#     def deactivate(location):

#         location.is_active = False
#         location.save(update_fields=[
#             "is_active",
#             "updated_at"
#         ])
#         return location


from django.db import IntegrityError, transaction
from rest_framework.exceptions import ValidationError

from apps.inventory.models.storage_location import StorageLocation


class StorageLocationService:

    @staticmethod
    @transaction.atomic
    def create(data):

        warehouse = data.get("warehouse")
        plant = data.get("plant")
        company = data.get("company")

        StorageLocationService._validate_relations(
            company=company,
            plant=plant,
            warehouse=warehouse
        )

        try:

            return StorageLocation.objects.create(
                **data
            )

        except IntegrityError:

            raise ValidationError(
                "Storage location code already exists in this warehouse."
            )

    @staticmethod
    @transaction.atomic
    def update(location, data):

        company = data.get(
            "company",
            location.company
        )

        plant = data.get(
            "plant",
            location.plant
        )

        warehouse = data.get(
            "warehouse",
            location.warehouse
        )

        StorageLocationService._validate_relations(
            company=company,
            plant=plant,
            warehouse=warehouse
        )

        try:

            for field, value in data.items():
                setattr(location, field, value)

            location.save()

            return location

        except IntegrityError:

            raise ValidationError(
                "Storage location code already exists in this warehouse."
            )

    @staticmethod
    def _validate_relations(
        *,
        company,
        plant,
        warehouse
    ):

        if not company:
            raise ValidationError(
                "Company is required."
            )

        if not plant:
            raise ValidationError(
                "Plant is required."
            )

        if not warehouse:
            raise ValidationError(
                "Warehouse is required."
            )

        if plant.company_id != company.id:

            raise ValidationError(
                "Plant does not belong to selected company."
            )

        if warehouse.company_id != company.id:

            raise ValidationError(
                "Warehouse does not belong to selected company."
            )

        if warehouse.plant_id != plant.id:

            raise ValidationError(
                "Warehouse does not belong to selected plant."
            )

        if not warehouse.is_active:

            raise ValidationError(
                "Warehouse is inactive."
            )

    @staticmethod
    def get_by_id(location_id):

        try:

            return StorageLocation.objects.select_related(
                "company",
                "plant",
                "warehouse"
            ).get(id=location_id)

        except StorageLocation.DoesNotExist:

            raise ValidationError(
                "Storage location not found."
            )

    @staticmethod
    def list(
        *,
        company_id=None,
        plant_id=None,
        warehouse_id=None,
        is_active=None
    ):

        queryset = StorageLocation.objects.select_related(
            "company",
            "plant",
            "warehouse"
        )

        if company_id:

            queryset = queryset.filter(
                company_id=company_id
            )

        if plant_id:

            queryset = queryset.filter(
                plant_id=plant_id
            )

        if warehouse_id:

            queryset = queryset.filter(
                warehouse_id=warehouse_id
            )

        if is_active is not None:

            queryset = queryset.filter(
                is_active=is_active
            )

        return queryset.order_by("code")

    @staticmethod
    @transaction.atomic
    def activate(location):

        location.is_active = True

        location.save(
            update_fields=[
                "is_active",
                "updated_at"
            ]
        )

        return location

    @staticmethod
    @transaction.atomic
    def deactivate(location):

        location.is_active = False

        location.save(
            update_fields=[
                "is_active",
                "updated_at"
            ]
        )

        return location