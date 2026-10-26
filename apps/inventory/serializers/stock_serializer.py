# from rest_framework import serializers

# from apps.inventory.models.stock import Stock


# class StockSerializer(serializers.ModelSerializer):

#     available_quantity = serializers.DecimalField(
#         max_digits=18,
#         decimal_places=3,
#         read_only=True
#     )

#     class Meta:
#         model = Stock

#         fields = [
#             "id",
#             "company",
#             "plant",
#             "item",
#             "warehouse",
#             "storage_location",
#             "batch",
#             "quantity",
#             "reserved_quantity",
#             "available_quantity",
#             "created_at",
#             "updated_at",
#         ]

#         read_only_fields = [
#             "id",
#             "quantity",
#             "available_quantity",
#             "created_at",
#             "updated_at",
#         ]
from rest_framework import serializers

from apps.inventory.models.stock import Stock


class StockSerializer(serializers.ModelSerializer):

    available_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Stock

        fields = [
            "id",
            "company",
            "plant",
            "item",
            "warehouse",
            "storage_location",
            "batch",
            "quantity",
            "reserved_quantity",
            "available_quantity",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "quantity",
            "reserved_quantity",
            "available_quantity",
            "created_at",
            "updated_at",
        ]

    def get_available_quantity(self, obj):

        return (
            obj.quantity -
            obj.reserved_quantity
        )