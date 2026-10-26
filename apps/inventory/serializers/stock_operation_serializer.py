# from rest_framework import serializers

# from apps.inventory.models.batch import Batch
# from apps.inventory.models.item import Item
# from apps.inventory.models.storage_location import StorageLocation
# from apps.inventory.models.warehouse import Warehouse

# from apps.masters.models.company import Company
# from apps.masters.models.plant import Plant


# # ============================================================
# # RECEIVE STOCK
# # ============================================================

# class ReceiveStockSerializer(serializers.Serializer):

#     company = serializers.PrimaryKeyRelatedField(
#         queryset=Company.objects.all()
#     )

#     plant = serializers.PrimaryKeyRelatedField(
#         queryset=Plant.objects.all()
#     )

#     item = serializers.PrimaryKeyRelatedField(
#         queryset=Item.objects.all()
#     )

#     warehouse = serializers.PrimaryKeyRelatedField(
#         queryset=Warehouse.objects.all()
#     )

#     storage_location = serializers.PrimaryKeyRelatedField(
#         queryset=StorageLocation.objects.all()
#     )

#     batch = serializers.PrimaryKeyRelatedField(
#         queryset=Batch.objects.all(),
#         required=False,
#         allow_null=True
#     )

#     quantity = serializers.DecimalField(
#         max_digits=18,
#         decimal_places=3,
#         min_value=0.001
#     )

#     reference_number = serializers.CharField(
#         max_length=100,
#         required=False,
#         allow_blank=True,
#         allow_null=True
#     )

#     remarks = serializers.CharField(
#         required=False,
#         allow_blank=True,
#         allow_null=True
#     )


# # ============================================================
# # ISSUE STOCK
# # ============================================================

# class IssueStockSerializer(serializers.Serializer):

#     company = serializers.PrimaryKeyRelatedField(
#         queryset=Company.objects.all()
#     )

#     plant = serializers.PrimaryKeyRelatedField(
#         queryset=Plant.objects.all()
#     )

#     item = serializers.PrimaryKeyRelatedField(
#         queryset=Item.objects.all()
#     )

#     warehouse = serializers.PrimaryKeyRelatedField(
#         queryset=Warehouse.objects.all()
#     )

#     storage_location = serializers.PrimaryKeyRelatedField(
#         queryset=StorageLocation.objects.all()
#     )

#     batch = serializers.PrimaryKeyRelatedField(
#         queryset=Batch.objects.all(),
#         required=False,
#         allow_null=True
#     )

#     quantity = serializers.DecimalField(
#         max_digits=18,
#         decimal_places=3,
#         min_value=0.001
#     )

#     reference_number = serializers.CharField(
#         max_length=100,
#         required=False,
#         allow_blank=True,
#         allow_null=True
#     )

#     remarks = serializers.CharField(
#         required=False,
#         allow_blank=True,
#         allow_null=True
#     )


# # ============================================================
# # TRANSFER STOCK
# # ============================================================

# class TransferStockSerializer(serializers.Serializer):

#     company = serializers.PrimaryKeyRelatedField(
#         queryset=Company.objects.all()
#     )

#     plant = serializers.PrimaryKeyRelatedField(
#         queryset=Plant.objects.all()
#     )

#     item = serializers.PrimaryKeyRelatedField(
#         queryset=Item.objects.all()
#     )

#     from_warehouse = serializers.PrimaryKeyRelatedField(
#         queryset=Warehouse.objects.all()
#     )

#     from_location = serializers.PrimaryKeyRelatedField(
#         queryset=StorageLocation.objects.all()
#     )

#     to_warehouse = serializers.PrimaryKeyRelatedField(
#         queryset=Warehouse.objects.all()
#     )

#     to_location = serializers.PrimaryKeyRelatedField(
#         queryset=StorageLocation.objects.all()
#     )

#     batch = serializers.PrimaryKeyRelatedField(
#         queryset=Batch.objects.all(),
#         required=False,
#         allow_null=True
#     )

#     quantity = serializers.DecimalField(
#         max_digits=18,
#         decimal_places=3,
#         min_value=0.001
#     )

#     reference_number = serializers.CharField(
#         max_length=100,
#         required=False,
#         allow_blank=True,
#         allow_null=True
#     )

#     remarks = serializers.CharField(
#         required=False,
#         allow_blank=True,
#         allow_null=True
#     )


# # ============================================================
# # STOCK ADJUSTMENT
# # ============================================================

# class AdjustmentSerializer(serializers.Serializer):

#     company = serializers.PrimaryKeyRelatedField(
#         queryset=Company.objects.all()
#     )

#     plant = serializers.PrimaryKeyRelatedField(
#         queryset=Plant.objects.all()
#     )

#     item = serializers.PrimaryKeyRelatedField(
#         queryset=Item.objects.all()
#     )

#     warehouse = serializers.PrimaryKeyRelatedField(
#         queryset=Warehouse.objects.all()
#     )

#     storage_location = serializers.PrimaryKeyRelatedField(
#         queryset=StorageLocation.objects.all()
#     )

#     batch = serializers.PrimaryKeyRelatedField(
#         queryset=Batch.objects.all(),
#         required=False,
#         allow_null=True
#     )

#     quantity = serializers.DecimalField(
#         max_digits=18,
#         decimal_places=3,
#         min_value=0.001
#     )

#     reference_number = serializers.CharField(
#         max_length=100,
#         required=False,
#         allow_blank=True,
#         allow_null=True
#     )

#     remarks = serializers.CharField(
#         required=False,
#         allow_blank=True,
#         allow_null=True
#     )
from rest_framework import serializers

from apps.inventory.models.batch import Batch
from apps.inventory.models.item import Item
from apps.inventory.models.storage_location import StorageLocation
from apps.inventory.models.warehouse import Warehouse

from apps.masters.models.company import Company
from apps.masters.models.plant import Plant


# ============================================================
# BASE STOCK OPERATION
# ============================================================

class BaseStockOperationSerializer(serializers.Serializer):

    company = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all()
    )

    plant = serializers.PrimaryKeyRelatedField(
        queryset=Plant.objects.all()
    )

    item = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.all()
    )

    warehouse = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all()
    )

    storage_location = serializers.PrimaryKeyRelatedField(
        queryset=StorageLocation.objects.all()
    )

    batch = serializers.PrimaryKeyRelatedField(
        queryset=Batch.objects.all(),
        required=False,
        allow_null=True
    )

    quantity = serializers.DecimalField(
        max_digits=18,
        decimal_places=3,
        min_value=0.001
    )

    reference_number = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        allow_null=True
    )

    remarks = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True
    )

    def validate(self, attrs):

        company = attrs["company"]
        plant = attrs["plant"]
        item = attrs["item"]
        warehouse = attrs["warehouse"]
        location = attrs["storage_location"]
        batch = attrs.get("batch")

        # ----------------------------------------------------
        # COMPANY
        # ----------------------------------------------------

        if plant.company_id != company.id:
            raise serializers.ValidationError(
                "Plant does not belong to selected company."
            )

        if item.company_id != company.id:
            raise serializers.ValidationError(
                "Item does not belong to selected company."
            )

        if warehouse.company_id != company.id:
            raise serializers.ValidationError(
                "Warehouse does not belong to selected company."
            )

        # ----------------------------------------------------
        # PLANT
        # ----------------------------------------------------

        if item.plant_id != plant.id:
            raise serializers.ValidationError(
                "Item does not belong to selected plant."
            )

        if warehouse.plant_id != plant.id:
            raise serializers.ValidationError(
                "Warehouse does not belong to selected plant."
            )

        # ----------------------------------------------------
        # STORAGE LOCATION
        # ----------------------------------------------------

        if location.warehouse_id != warehouse.id:
            raise serializers.ValidationError(
                "Storage location does not belong to selected warehouse."
            )

        # ----------------------------------------------------
        # ITEM ACTIVE
        # ----------------------------------------------------

        if hasattr(item, "is_active") and not item.is_active:
            raise serializers.ValidationError(
                "Item is inactive."
            )

        # ----------------------------------------------------
        # BATCH
        # ----------------------------------------------------

        if batch:

            if batch.item_id != item.id:
                raise serializers.ValidationError(
                    "Batch does not belong to selected item."
                )

            if batch.plant_id != plant.id:
                raise serializers.ValidationError(
                    "Batch does not belong to selected plant."
                )

            if batch.company_id != company.id:
                raise serializers.ValidationError(
                    "Batch does not belong to selected company."
                )

            if hasattr(batch, "is_active") and not batch.is_active:
                raise serializers.ValidationError(
                    "Batch is inactive."
                )

        return attrs


# ============================================================
# RECEIVE
# ============================================================

class ReceiveStockSerializer(BaseStockOperationSerializer):
    pass


# ============================================================
# ISSUE
# ============================================================

class IssueStockSerializer(BaseStockOperationSerializer):
    pass


# ============================================================
# ADJUSTMENT
# ============================================================

class AdjustmentSerializer(BaseStockOperationSerializer):

    adjustment_type = serializers.ChoiceField(
        choices=[
            ("adjustment_in", "Adjustment In"),
            ("adjustment_out", "Adjustment Out"),
        ]
    )


# ============================================================
# RETURN
# ============================================================

class ReturnStockSerializer(BaseStockOperationSerializer):
    pass


# ============================================================
# TRANSFER
# ============================================================

class TransferStockSerializer(serializers.Serializer):

    company = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all()
    )

    plant = serializers.PrimaryKeyRelatedField(
        queryset=Plant.objects.all()
    )

    item = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.all()
    )

    from_warehouse = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all()
    )

    from_location = serializers.PrimaryKeyRelatedField(
        queryset=StorageLocation.objects.all()
    )

    to_warehouse = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all()
    )

    to_location = serializers.PrimaryKeyRelatedField(
        queryset=StorageLocation.objects.all()
    )

    batch = serializers.PrimaryKeyRelatedField(
        queryset=Batch.objects.all(),
        required=False,
        allow_null=True
    )

    quantity = serializers.DecimalField(
        max_digits=18,
        decimal_places=3,
        min_value=0.001
    )

    reference_number = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        allow_null=True
    )

    remarks = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True
    )

    def validate(self, attrs):

        company = attrs["company"]
        plant = attrs["plant"]
        item = attrs["item"]

        from_warehouse = attrs["from_warehouse"]
        from_location = attrs["from_location"]

        to_warehouse = attrs["to_warehouse"]
        to_location = attrs["to_location"]

        batch = attrs.get("batch")

        # ----------------------------------------------------
        # COMPANY
        # ----------------------------------------------------

        if plant.company_id != company.id:
            raise serializers.ValidationError(
                "Plant does not belong to selected company."
            )

        if item.company_id != company.id:
            raise serializers.ValidationError(
                "Item does not belong to selected company."
            )

        if from_warehouse.company_id != company.id:
            raise serializers.ValidationError(
                "Source warehouse does not belong to selected company."
            )

        if to_warehouse.company_id != company.id:
            raise serializers.ValidationError(
                "Destination warehouse does not belong to selected company."
            )

        # ----------------------------------------------------
        # PLANT
        # ----------------------------------------------------

        if item.plant_id != plant.id:
            raise serializers.ValidationError(
                "Item does not belong to selected plant."
            )

        if from_warehouse.plant_id != plant.id:
            raise serializers.ValidationError(
                "Source warehouse does not belong to selected plant."
            )

        if to_warehouse.plant_id != plant.id:
            raise serializers.ValidationError(
                "Destination warehouse does not belong to selected plant."
            )

        # ----------------------------------------------------
        # LOCATIONS
        # ----------------------------------------------------

        if from_location.warehouse_id != from_warehouse.id:
            raise serializers.ValidationError(
                "Source location does not belong to source warehouse."
            )

        if to_location.warehouse_id != to_warehouse.id:
            raise serializers.ValidationError(
                "Destination location does not belong to destination warehouse."
            )

        # ----------------------------------------------------
        # SAME LOCATION
        # ----------------------------------------------------

        if (
            from_warehouse.id == to_warehouse.id
            and from_location.id == to_location.id
        ):
            raise serializers.ValidationError(
                "Source and destination cannot be the same."
            )

        # ----------------------------------------------------
        # BATCH
        # ----------------------------------------------------

        if batch:

            if batch.item_id != item.id:
                raise serializers.ValidationError(
                    "Batch does not belong to selected item."
                )

            if batch.plant_id != plant.id:
                raise serializers.ValidationError(
                    "Batch does not belong to selected plant."
                )

            if batch.company_id != company.id:
                raise serializers.ValidationError(
                    "Batch does not belong to selected company."
                )

        return attrs