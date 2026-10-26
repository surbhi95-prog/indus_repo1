# from rest_framework import serializers

# from apps.inventory.models.warehouse import Warehouse


# class WarehouseSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Warehouse

#         fields = [
#             "id",
#             "company",
#             "plant",
#             "code",
#             "name",
#             "description",
#             "warehouse_type",
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

#         company = attrs.get("company")
#         plant = attrs.get("plant")

#         if company and plant:
#             if plant.company_id != company.id:
#                 raise serializers.ValidationError(
#                     "Plant does not belong to the selected company."
#                 )

#         return attrs
    


from rest_framework import serializers

from apps.inventory.models.warehouse import Warehouse


class WarehouseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Warehouse

        fields = [
            "id",
            "company",
            "plant",
            "code",
            "name",
            "description",
            "warehouse_type",
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

        if company and plant:

            if plant.company_id != company.id:
                raise serializers.ValidationError({
                    "plant":
                        "Plant does not belong to the selected company."
                })

        return attrs