# from django.db import transaction

# from apps.masters.models.department import Department


# class DepartmentService:

#     @staticmethod
#     @transaction.atomic
#     def create_department(data):

#         return Department.objects.create(
#             **data
#         )

#     @staticmethod
#     def get_all_departments():

#         return Department.objects.select_related(
#             "plant",
#             "plant__company"
#         ).all()

#     @staticmethod
#     def get_department(department_id):

#         return Department.objects.select_related(
#             "plant",
#             "plant__company"
#         ).get(
#             id=department_id
#         )

#     @staticmethod
#     @transaction.atomic
#     def update_department(department, data):

#         for field, value in data.items():

#             setattr(
#                 department,
#                 field,
#                 value
#             )

#         department.save()

#         return department

#     @staticmethod
#     @transaction.atomic
#     def delete_department(department):

#         department.delete()
from django.db import transaction
from django.shortcuts import get_object_or_404

from apps.masters.models.department import Department


class DepartmentService:

    # =========================================================
    # CREATE
    # =========================================================

    @staticmethod
    @transaction.atomic
    def create_department(validated_data):

        return Department.objects.create(
            **validated_data
        )

    # =========================================================
    # GET ALL
    # =========================================================

    @staticmethod
    def get_all_departments(
        company_id=None,
        plant_id=None
    ):

        queryset = Department.objects.select_related(
            "company",
            "plant"
        ).filter(
            is_active=True
        )

        # -----------------------------------------------------
        # COMPANY FILTER
        # -----------------------------------------------------

        if company_id:
            queryset = queryset.filter(
                company_id=company_id
            )

        # -----------------------------------------------------
        # PLANT FILTER
        # -----------------------------------------------------

        if plant_id:
            queryset = queryset.filter(
                plant_id=plant_id
            )

        return queryset.order_by("name")

    # =========================================================
    # GET SINGLE
    # =========================================================

    @staticmethod
    def get_department(department_id):

        return get_object_or_404(
            Department.objects.select_related(
                "company",
                "plant"
            ),
            id=department_id,
            is_active=True
        )

    # =========================================================
    # UPDATE
    # =========================================================

    @staticmethod
    @transaction.atomic
    def update_department(
        department,
        validated_data
    ):

        for field, value in validated_data.items():

            setattr(
                department,
                field,
                value
            )

        department.save()

        return department

    # =========================================================
    # DELETE - SOFT DELETE
    # =========================================================

    @staticmethod
    @transaction.atomic
    def delete_department(department):

        department.is_active = False

        department.save(
            update_fields=[
                "is_active",
                "updated_at"
            ]
        )

        return department