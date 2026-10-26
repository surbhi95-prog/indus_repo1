# from django.db import IntegrityError, transaction
# from rest_framework.exceptions import ValidationError

# from apps.inventory.models.item import Item


# class ItemService:

#     @staticmethod
#     @transaction.atomic
#     def create(data):

#         category = data.get("category")
#         uom = data.get("uom")
#         plant = data.get("plant")
#         company = data.get("company")

#         ItemService._validate_relations(
#             company=company,
#             plant=plant,
#             category=category,
#             uom=uom
#         )

#         try:
#             return Item.objects.create(**data)

#         except IntegrityError:
#             raise ValidationError(
#                 "Item code already exists for this plant."
#             )

#     @staticmethod
#     @transaction.atomic
#     def update(item, data):

#         category = data.get(
#             "category",
#             item.category
#         )

#         uom = data.get(
#             "uom",
#             item.uom
#         )

#         plant = data.get(
#             "plant",
#             item.plant
#         )

#         company = data.get(
#             "company",
#             item.company
#         )

#         ItemService._validate_relations(
#             company=company,
#             plant=plant,
#             category=category,
#             uom=uom
#         )

#         try:

#             for field, value in data.items():
#                 setattr(item, field, value)

#             item.save()

#             return item

#         except IntegrityError:
#             raise ValidationError(
#                 "Item code already exists for this plant."
#             )

#     @staticmethod
#     def _validate_relations(
#         *,
#         company,
#         plant,
#         category,
#         uom
#     ):

#         if not plant:
#             raise ValidationError(
#                 "Plant is required."
#             )

#         if not company:
#             raise ValidationError(
#                 "Company is required."
#             )

#         if plant.company_id != company.id:
#             raise ValidationError(
#                 "Plant does not belong to selected company."
#             )

#         if category.plant_id != plant.id:
#             raise ValidationError(
#                 "Category does not belong to selected plant."
#             )

#         if category.company_id != company.id:
#             raise ValidationError(
#                 "Category does not belong to selected company."
#             )

#         if uom.plant_id != plant.id:
#             raise ValidationError(
#                 "UOM does not belong to selected plant."
#             )

#         if uom.company_id != company.id:
#             raise ValidationError(
#                 "UOM does not belong to selected company."
#             )

#         if not category.is_active:
#             raise ValidationError(
#                 "Category is inactive."
#             )

#         if not uom.is_active:
#             raise ValidationError(
#                 "UOM is inactive."
#             )

#     @staticmethod
#     def get_by_id(item_id):

#         try:
#             return Item.objects.select_related(
#                 "company",
#                 "plant",
#                 "category",
#                 "uom"
#             ).get(id=item_id)

#         except Item.DoesNotExist:
#             raise ValidationError(
#                 "Item not found."
#             )

#     @staticmethod
#     def list(
#         *,
#         company_id=None,
#         plant_id=None,
#         category_id=None,
#         item_type=None,
#         is_active=None
#     ):

#         queryset = Item.objects.select_related(
#             "company",
#             "plant",
#             "category",
#             "uom"
#         )

#         if company_id:
#             queryset = queryset.filter(
#                 company_id=company_id
#             )

#         if plant_id:
#             queryset = queryset.filter(
#                 plant_id=plant_id
#             )

#         if category_id:
#             queryset = queryset.filter(
#                 category_id=category_id
#             )

#         if item_type:
#             queryset = queryset.filter(
#                 item_type=item_type
#             )

#         if is_active is not None:
#             queryset = queryset.filter(
#                 is_active=is_active
#             )

#         return queryset.order_by("name")

#     @staticmethod
#     @transaction.atomic
#     def activate(item):

#         item.is_active = True
#         item.save(update_fields=[
#             "is_active",
#             "updated_at"
#         ])

#         return item

#     @staticmethod
#     @transaction.atomic
#     def deactivate(item):

#         item.is_active = False
#         item.save(update_fields=[
#             "is_active",
#             "updated_at"
#         ])

#         return item




from django.db import IntegrityError, transaction
from django.db.models import Q
from rest_framework.exceptions import ValidationError

from apps.inventory.models.item import Item


class ItemService:

    @staticmethod
    @transaction.atomic
    def create(data):

        category = data.get("category")
        uom = data.get("uom")
        plant = data.get("plant")
        company = data.get("company")

        ItemService._validate_relations(
            company=company,
            plant=plant,
            category=category,
            uom=uom
        )

        try:

            return Item.objects.create(**data)

        except IntegrityError:

            raise ValidationError(
                "Item code already exists for this plant."
            )

    @staticmethod
    @transaction.atomic
    def update(item, data):

        category = data.get(
            "category",
            item.category
        )

        uom = data.get(
            "uom",
            item.uom
        )

        plant = data.get(
            "plant",
            item.plant
        )

        company = data.get(
            "company",
            item.company
        )

        ItemService._validate_relations(
            company=company,
            plant=plant,
            category=category,
            uom=uom
        )

        try:

            for field, value in data.items():
                setattr(item, field, value)

            item.save()

            return item

        except IntegrityError:

            raise ValidationError(
                "Item code already exists for this plant."
            )

    @staticmethod
    def _validate_relations(
        *,
        company,
        plant,
        category,
        uom
    ):

        if not plant:
            raise ValidationError(
                "Plant is required."
            )

        if not company:
            raise ValidationError(
                "Company is required."
            )

        if not category:
            raise ValidationError(
                "Category is required."
            )

        if not uom:
            raise ValidationError(
                "UOM is required."
            )

        if plant.company_id != company.id:

            raise ValidationError(
                "Plant does not belong to selected company."
            )

        if category.plant_id != plant.id:

            raise ValidationError(
                "Category does not belong to selected plant."
            )

        if category.company_id != company.id:

            raise ValidationError(
                "Category does not belong to selected company."
            )

        if uom.plant_id != plant.id:

            raise ValidationError(
                "UOM does not belong to selected plant."
            )

        if uom.company_id != company.id:

            raise ValidationError(
                "UOM does not belong to selected company."
            )

        if not category.is_active:

            raise ValidationError(
                "Category is inactive."
            )

        if not uom.is_active:

            raise ValidationError(
                "UOM is inactive."
            )

    @staticmethod
    def get_by_id(item_id):

        try:

            return Item.objects.select_related(
                "company",
                "plant",
                "category",
                "uom"
            ).get(id=item_id)

        except Item.DoesNotExist:

            raise ValidationError(
                "Item not found."
            )

    @staticmethod
    def list(
        *,
        company_id=None,
        plant_id=None,
        category_id=None,
        uom_id=None,
        item_type=None,
        is_active=None,
        search=None
    ):

        queryset = Item.objects.select_related(
            "company",
            "plant",
            "category",
            "uom"
        )

        if company_id:

            queryset = queryset.filter(
                company_id=company_id
            )

        if plant_id:

            queryset = queryset.filter(
                plant_id=plant_id
            )

        if category_id:

            queryset = queryset.filter(
                category_id=category_id
            )

        if uom_id:

            queryset = queryset.filter(
                uom_id=uom_id
            )

        if item_type:

            queryset = queryset.filter(
                item_type=item_type
            )

        if is_active is not None:

            queryset = queryset.filter(
                is_active=is_active
            )

        if search:

            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(code__icontains=search) |
                Q(description__icontains=search)
            )

        return queryset.order_by("name")

    @staticmethod
    @transaction.atomic
    def activate(item):

        item.is_active = True

        item.save(
            update_fields=[
                "is_active",
                "updated_at"
            ]
        )

        return item

    @staticmethod
    @transaction.atomic
    def deactivate(item):

        item.is_active = False

        item.save(
            update_fields=[
                "is_active",
                "updated_at"
            ]
        )

        return item