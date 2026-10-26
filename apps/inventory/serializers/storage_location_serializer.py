# from rest_framework import serializers

# from apps.inventory.models.storage_location import StorageLocation


# class StorageLocationSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = StorageLocation

#         fields = [
#             "id",
#             "company",
#             "plant",
#             "warehouse",
#             "code",
#             "name",
#             "description",
#             "rack",
#             "bin",
#             "is_active",
#             "created_at",
#             "updated_at",
#         ]

#         read_only_fields = [
#             "id",
#             "created_at",
#             "updated_at",
#         ]

#     def validate(self, attrs):

#         plant = attrs.get("plant")
#         warehouse = attrs.get("warehouse")

#         if plant and warehouse:

#             if warehouse.plant_id != plant.id:
#                 raise serializers.ValidationError(
#                     "Warehouse does not belong to the selected plant."
#                 )

#         company = attrs.get("company")

#         if company and warehouse:

#             if warehouse.company_id != company.id:
#                 raise serializers.ValidationError(
#                     "Warehouse does not belong to the selected company."
#                 )

#         return attrs

from rest_framework import serializers

from apps.inventory.models.storage_location import StorageLocation


class StorageLocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = StorageLocation

        fields = [
            "id",
            "company",
            "plant",
            "warehouse",
            "code",
            "name",
            "description",
            "rack",
            "bin",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):

        company = attrs.get(
            "company",
            getattr(self.instance, "company", None)
        )

        plant = attrs.get(
            "plant",
            getattr(self.instance, "plant", None)
        )

        warehouse = attrs.get(
            "warehouse",
            getattr(self.instance, "warehouse", None)
        )

        if company and plant:

            if plant.company_id != company.id:
                raise serializers.ValidationError({
                    "plant":
                        "Plant does not belong to the selected company."
                })

        if company and warehouse:

            if warehouse.company_id != company.id:
                raise serializers.ValidationError({
                    "warehouse":
                        "Warehouse does not belong to the selected company."
                })

        if plant and warehouse:

            if warehouse.plant_id != plant.id:
                raise serializers.ValidationError({
                    "warehouse":
                        "Warehouse does not belong to the selected plant."
                })

        return attrs