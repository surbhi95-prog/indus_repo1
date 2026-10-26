# from django.db import IntegrityError, transaction
# from rest_framework.exceptions import ValidationError

# from apps.inventory.models.warehouse import Warehouse


# class WarehouseService:

#     @staticmethod
#     @transaction.atomic
#     def create(data):

#         company = data.get("company")
#         plant = data.get("plant")

#         WarehouseService._validate_organization(
#             company,
#             plant
#         )

#         try:
#             return Warehouse.objects.create(**data)

#         except IntegrityError:
#             raise ValidationError(
#                 "Warehouse code already exists for this plant."
#             )

#     @staticmethod
#     @transaction.atomic
#     def update(warehouse, data):

#         company = data.get(
#             "company",
#             warehouse.company
#         )

#         plant = data.get(
#             "plant",
#             warehouse.plant
#         )

#         WarehouseService._validate_organization(
#             company,
#             plant
#         )

#         try:

#             for field, value in data.items():
#                 setattr(warehouse, field, value)

#             warehouse.save()

#             return warehouse

#         except IntegrityError:
#             raise ValidationError(
#                 "Warehouse code already exists for this plant."
#             )

#     @staticmethod
#     def _validate_organization(company, plant):

#         if not company:
#             raise ValidationError(
#                 "Company is required."
#             )

#         if not plant:
#             raise ValidationError(
#                 "Plant is required."
#             )

#         if plant.company_id != company.id:
#             raise ValidationError(
#                 "Plant does not belong to selected company."
#             )

#     @staticmethod
#     def get_by_id(warehouse_id):

#         try:
#             return Warehouse.objects.select_related(
#                 "company",
#                 "plant"
#             ).get(id=warehouse_id)

#         except Warehouse.DoesNotExist:
#             raise ValidationError(
#                 "Warehouse not found."
#             )

#     @staticmethod
#     def list(
#         *,
#         company_id=None,
#         plant_id=None,
#         warehouse_type=None,
#         is_active=None
#     ):

#         queryset = Warehouse.objects.select_related(
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

#         if warehouse_type:
#             queryset = queryset.filter(
#                 warehouse_type=warehouse_type
#             )

#         if is_active is not None:
#             queryset = queryset.filter(
#                 is_active=is_active
#             )

#         return queryset.order_by("name")

#     @staticmethod
#     @transaction.atomic
#     def activate(warehouse):

#         warehouse.is_active = True
#         warehouse.save(update_fields=[
#             "is_active",
#             "updated_at"
#         ])

#         return warehouse

#     @staticmethod
#     @transaction.atomic
#     def deactivate(warehouse):

#         warehouse.is_active = False
#         warehouse.save(update_fields=[
#             "is_active",
#             "updated_at"
#         ])

#         return warehouse


from django.db import IntegrityError, transaction
from rest_framework.exceptions import ValidationError

from apps.inventory.models.warehouse import Warehouse


class WarehouseService:

    @staticmethod
    @transaction.atomic
    def create(data):

        company = data.get("company")
        plant = data.get("plant")

        WarehouseService._validate_organization(
            company,
            plant
        )

        try:
            return Warehouse.objects.create(**data)

        except IntegrityError:
            raise ValidationError(
                "Warehouse code already exists for this plant."
            )

    @staticmethod
    @transaction.atomic
    def update(warehouse, data):

        company = data.get(
            "company",
            warehouse.company
        )

        plant = data.get(
            "plant",
            warehouse.plant
        )

        WarehouseService._validate_organization(
            company,
            plant
        )

        try:

            for field, value in data.items():
                setattr(warehouse, field, value)

            warehouse.save()

            return warehouse

        except IntegrityError:
            raise ValidationError(
                "Warehouse code already exists for this plant."
            )

    @staticmethod
    def _validate_organization(company, plant):

        if not company:
            raise ValidationError(
                "Company is required."
            )

        if not plant:
            raise ValidationError(
                "Plant is required."
            )

        if plant.company_id != company.id:
            raise ValidationError(
                "Plant does not belong to selected company."
            )

    @staticmethod
    def get_by_id(warehouse_id):

        try:
            return Warehouse.objects.select_related(
                "company",
                "plant"
            ).get(id=warehouse_id)

        except Warehouse.DoesNotExist:
            raise ValidationError(
                "Warehouse not found."
            )

    @staticmethod
    def list(
        *,
        company_id=None,
        plant_id=None,
        warehouse_type=None,
        is_active=None
    ):

        queryset = Warehouse.objects.select_related(
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

        if warehouse_type:
            queryset = queryset.filter(
                warehouse_type=warehouse_type
            )

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active
            )

        return queryset.order_by("name")

    @staticmethod
    @transaction.atomic
    def activate(warehouse):

        warehouse.is_active = True

        warehouse.save(
            update_fields=[
                "is_active",
                "updated_at"
            ]
        )

        return warehouse

    @staticmethod
    @transaction.atomic
    def deactivate(warehouse):

        warehouse.is_active = False

        warehouse.save(
            update_fields=[
                "is_active",
                "updated_at"
            ]
        )

        return warehouse