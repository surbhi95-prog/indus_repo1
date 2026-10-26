# from django.db import transaction

# from apps.masters.models.plant import Plant


# class PlantService:

#     @staticmethod
#     @transaction.atomic
#     def create_plant(data):

#         return Plant.objects.create(
#             **data
#         )


#     @staticmethod
#     def get_all_plants():

#         return Plant.objects.select_related(
#             "company"
#         ).all()


#     @staticmethod
#     def get_plant(plant_id):

#         return Plant.objects.select_related(
#             "company"
#         ).get(
#             id=plant_id
#         )


#     @staticmethod
#     @transaction.atomic
#     def update_plant(plant, data):

#         for field, value in data.items():
#             setattr(
#                 plant,
#                 field,
#                 value
#             )

#         plant.save()

#         return plant


#     @staticmethod
#     @transaction.atomic
#     def delete_plant(plant):

#         plant.delete()


from django.db import transaction
from django.shortcuts import get_object_or_404

from apps.masters.models.plant import Plant
from apps.masters.models.department import Department
from apps.hrms.models.employee import Employee


class PlantService:

    # =========================================================
    # CREATE
    # =========================================================

    @staticmethod
    @transaction.atomic
    def create_plant(validated_data):

        address_data = validated_data.pop(
            "address",
            {}
        )

        contact_data = validated_data.pop(
            "contact",
            {}
        )

        plant = Plant.objects.create(
            **validated_data,
            **address_data,
            **contact_data
        )

        return plant

    # =========================================================
    # GET ALL
    # =========================================================

    @staticmethod
    def get_all_plants(company_id=None):

        queryset = Plant.objects.select_related(
            "company"
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

        return queryset.order_by(
            "name"
        )

    # =========================================================
    # GET SINGLE
    # =========================================================

    @staticmethod
    def get_plant(plant_id):

        return get_object_or_404(
            Plant.objects.select_related(
                "company"
            ),
            id=plant_id,
            is_active=True
        )

    @staticmethod
    def get_plant_details(plant_id):
        plant = PlantService.get_plant(plant_id)
        plant.employee_count = Employee.objects.filter(
            plant_id=plant.id,
            status="active",
        ).count()
        plant.department_count = Department.objects.filter(
            plant_id=plant.id,
            is_active=True,
        ).count()
        return plant

    # =========================================================
    # UPDATE
    # =========================================================

    @staticmethod
    @transaction.atomic
    def update_plant(plant, validated_data):

        address_data = validated_data.pop(
            "address",
            None
        )

        contact_data = validated_data.pop(
            "contact",
            None
        )

        # -----------------------------------------------------
        # NORMAL FIELDS
        # -----------------------------------------------------

        for field, value in validated_data.items():

            setattr(
                plant,
                field,
                value
            )

        # -----------------------------------------------------
        # ADDRESS
        # -----------------------------------------------------

        if address_data is not None:

            for field, value in address_data.items():

                setattr(
                    plant,
                    field,
                    value
                )

        # -----------------------------------------------------
        # CONTACT
        # -----------------------------------------------------

        if contact_data is not None:

            for field, value in contact_data.items():

                setattr(
                    plant,
                    field,
                    value
                )

        plant.save()

        return plant

    # =========================================================
    # DELETE
    # =========================================================

    @staticmethod
    @transaction.atomic
    def delete_plant(plant):

        plant.is_active = False

        plant.save(
            update_fields=[
                "is_active",
                "updated_at"
            ]
        )

        return plant
