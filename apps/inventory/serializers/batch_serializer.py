from rest_framework import serializers

from apps.inventory.models.batch import Batch


class BatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Batch

        fields = [
            "id",
            "company",
            "plant",
            "item",
            "batch_number",
            "manufacture_date",
            "expiry_date",
            "is_active",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]

    def validate(self, attrs):

        manufacture_date = attrs.get("manufacture_date")
        expiry_date = attrs.get("expiry_date")

        if (
            manufacture_date
            and expiry_date
            and expiry_date < manufacture_date
        ):
            raise serializers.ValidationError(
                "Expiry date cannot be before manufacture date."
            )

        item = attrs.get("item")
        plant = attrs.get("plant")

        if item and plant:
            if item.plant_id != plant.id:
                raise serializers.ValidationError(
                    "Item does not belong to the selected plant."
                )

        return attrs