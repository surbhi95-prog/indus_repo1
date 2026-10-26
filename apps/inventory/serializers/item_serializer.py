# from rest_framework import serializers

# from apps.inventory.models.item import Item


# class ItemSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Item

#         fields = [
#             "id",
#             "company",
#             "plant",
#             "category",
#             "uom",
#             "code",
#             "name",
#             "item_type",
#             "description",
#             "minimum_stock",
#             "maximum_stock",
#             "is_batch_required",
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

#         category = attrs.get("category")
#         uom = attrs.get("uom")
#         plant = attrs.get("plant")

#         if category and plant:
#             if category.plant_id != plant.id:
#                 raise serializers.ValidationError(
#                     "Category does not belong to the selected plant."
#                 )

#         if uom and plant:
#             if uom.plant_id != plant.id:
#                 raise serializers.ValidationError(
#                     "UOM does not belong to the selected plant."
#                 )

#         minimum = attrs.get("minimum_stock")
#         maximum = attrs.get("maximum_stock")

#         if minimum is not None and maximum is not None:
#             if maximum < minimum:
#                 raise serializers.ValidationError(
#                     "Maximum stock cannot be less than minimum stock."
#                 )

#         return attrs    



from rest_framework import serializers

from apps.inventory.models.item import Item


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item

        fields = [
            "id",
            "company",
            "plant",
            "category",
            "uom",
            "code",
            "name",
            "item_type",
            "description",
            "minimum_stock",
            "maximum_stock",
            "is_batch_required",
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

        category = attrs.get(
            "category",
            getattr(self.instance, "category", None)
        )

        uom = attrs.get(
            "uom",
            getattr(self.instance, "uom", None)
        )

        if plant and company:

            if plant.company_id != company.id:
                raise serializers.ValidationError({
                    "plant": "Plant does not belong to the selected company."
                })

        if category and plant:

            if category.plant_id != plant.id:
                raise serializers.ValidationError({
                    "category": "Category does not belong to the selected plant."
                })

        if category and company:

            if category.company_id != company.id:
                raise serializers.ValidationError({
                    "category": "Category does not belong to the selected company."
                })

        if uom and plant:

            if uom.plant_id != plant.id:
                raise serializers.ValidationError({
                    "uom": "UOM does not belong to the selected plant."
                })

        if uom and company:

            if uom.company_id != company.id:
                raise serializers.ValidationError({
                    "uom": "UOM does not belong to the selected company."
                })

        minimum = attrs.get(
            "minimum_stock",
            getattr(self.instance, "minimum_stock", None)
        )

        maximum = attrs.get(
            "maximum_stock",
            getattr(self.instance, "maximum_stock", None)
        )

        if minimum is not None and maximum is not None:

            if maximum < minimum:
                raise serializers.ValidationError({
                    "maximum_stock":
                        "Maximum stock cannot be less than minimum stock."
                })

        return attrs