# from rest_framework import serializers

# from apps.inventory.models.stock_movement import StockMovement


# class StockMovementSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = StockMovement

#         fields = [
#             "id",
#             "company",
#             "plant",
#             "item",
#             "batch",
#             "movement_type",
#             "quantity",
#             "from_warehouse",
#             "from_location",
#             "to_warehouse",
#             "to_location",
#             "reference_number",
#             "remarks",
#             "created_at",
#         ]

#         read_only_fields = [
#             "id",
#             "created_at",
#         ]

#     def validate(self, attrs):

#         quantity = attrs.get("quantity")

#         if quantity is not None and quantity <= 0:
#             raise serializers.ValidationError(
#                 "Quantity must be greater than zero."
#             )

#         item = attrs.get("item")
#         batch = attrs.get("batch")

#         if batch and item:
#             if batch.item_id != item.id:
#                 raise serializers.ValidationError(
#                     "Batch does not belong to the selected item."
#                 )

#         return attrs


from rest_framework import serializers

from apps.inventory.models.stock_movement import StockMovement


class StockMovementSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockMovement

        fields = [
            "id",
            "company",
            "plant",
            "item",
            "batch",
            "movement_type",
            "quantity",
            "from_warehouse",
            "from_location",
            "to_warehouse",
            "to_location",
            "reference_number",
            "remarks",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]

    def validate(self, attrs):

        quantity = attrs.get("quantity")

        if quantity is not None and quantity <= 0:
            raise serializers.ValidationError(
                "Quantity must be greater than zero."
            )

        item = attrs.get("item")
        batch = attrs.get("batch")

        if batch and item:

            if batch.item_id != item.id:
                raise serializers.ValidationError(
                    "Batch does not belong to the selected item."
                )

            if batch.plant_id != item.plant_id:
                raise serializers.ValidationError(
                    "Batch does not belong to the selected item's plant."
                )

            if batch.company_id != item.company_id:
                raise serializers.ValidationError(
                    "Batch does not belong to the selected item's company."
                )

        return attrs