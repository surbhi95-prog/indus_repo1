from django.db import IntegrityError, transaction
from rest_framework.exceptions import ValidationError

from apps.inventory.models.category import Category


class CategoryService:

    @staticmethod
    @transaction.atomic
    def create(data):
        try:
            return Category.objects.create(**data)
        except IntegrityError:
            raise ValidationError(
                "Category code already exists for this plant."
            )

    @staticmethod
    @transaction.atomic
    def update(category, data):
        try:
            for field, value in data.items():
                setattr(category, field, value)

            category.save()

            return category

        except IntegrityError:
            raise ValidationError(
                "Category code already exists for this plant."
            )

    @staticmethod
    def get_by_id(category_id):
        try:
            return Category.objects.select_related(
                "company",
                "plant"
            ).get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError(
                "Category not found."
            )

    @staticmethod
    def list(
        *,
        company_id=None,
        plant_id=None,
        is_active=None
    ):
        queryset = Category.objects.select_related(
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
    def deactivate(category):
        category.is_active = False
        category.save(update_fields=["is_active", "updated_at"])

        return category

    @staticmethod
    @transaction.atomic
    def activate(category):
        category.is_active = True
        category.save(update_fields=["is_active", "updated_at"])

        return category