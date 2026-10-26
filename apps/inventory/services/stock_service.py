# from decimal import Decimal

# from django.db import transaction
# from django.db.models import F
# from rest_framework.exceptions import ValidationError

# from apps.inventory.models.stock import Stock
# from apps.inventory.models.stock_movement import StockMovement


# class StockService:

#     @staticmethod
#     def _validate_quantity(quantity):

#         quantity = Decimal(str(quantity))

#         if quantity <= 0:
#             raise ValidationError(
#                 "Quantity must be greater than zero."
#             )

#         return quantity

#     @staticmethod
#     def _validate_item(item, batch=None):

#         if not item.is_active:
#             raise ValidationError(
#                 "Item is inactive."
#             )

#         if item.is_batch_required and batch is None:
#             raise ValidationError(
#                 "Batch is required for this item."
#             )

#         if batch:

#             if batch.item_id != item.id:
#                 raise ValidationError(
#                     "Batch does not belong to selected item."
#                 )

#             if not batch.is_active:
#                 raise ValidationError(
#                     "Batch is inactive."
#                 )

#     @staticmethod
#     def _validate_location(
#         *,
#         warehouse,
#         storage_location
#     ):

#         if not warehouse.is_active:
#             raise ValidationError(
#                 "Warehouse is inactive."
#             )

#         if not storage_location.is_active:
#             raise ValidationError(
#                 "Storage location is inactive."
#             )

#         if storage_location.warehouse_id != warehouse.id:
#             raise ValidationError(
#                 "Storage location does not belong to warehouse."
#             )

#     @staticmethod
#     @transaction.atomic
#     def receive_stock(
#         *,
#         company,
#         plant,
#         item,
#         warehouse,
#         storage_location,
#         quantity,
#         batch=None,
#         reference_number=None,
#         remarks=None
#     ):

#         quantity = StockService._validate_quantity(
#             quantity
#         )

#         StockService._validate_item(
#             item,
#             batch
#         )

#         StockService._validate_location(
#             warehouse=warehouse,
#             storage_location=storage_location
#         )

#         stock, _ = Stock.objects.select_for_update().get_or_create(
#             company=company,
#             plant=plant,
#             item=item,
#             warehouse=warehouse,
#             storage_location=storage_location,
#             batch=batch,
#             defaults={
#                 "quantity": Decimal("0"),
#                 "reserved_quantity": Decimal("0")
#             }
#         )

#         previous_quantity = stock.quantity

#         stock.quantity = F("quantity") + quantity

#         stock.save(
#             update_fields=[
#                 "quantity",
#                 "updated_at"
#             ]
#         )

#         stock.refresh_from_db()

#         movement = StockMovement.objects.create(
#             company=company,
#             plant=plant,
#             item=item,
#             batch=batch,
#             movement_type="receipt",
#             quantity=quantity,
#             to_warehouse=warehouse,
#             to_location=storage_location,
#             reference_number=reference_number,
#             remarks=remarks
#         )

#         return {
#             "stock": stock,
#             "movement": movement,
#             "previous_quantity": previous_quantity,
#             "new_quantity": stock.quantity
#         }

#     @staticmethod
#     @transaction.atomic
#     def issue_stock(
#         *,
#         company,
#         plant,
#         item,
#         warehouse,
#         storage_location,
#         quantity,
#         batch=None,
#         reference_number=None,
#         remarks=None
#     ):

#         quantity = StockService._validate_quantity(
#             quantity
#         )

#         StockService._validate_item(
#             item,
#             batch
#         )

#         StockService._validate_location(
#             warehouse=warehouse,
#             storage_location=storage_location
#         )

#         try:

#             stock = Stock.objects.select_for_update().get(
#                 company=company,
#                 plant=plant,
#                 item=item,
#                 warehouse=warehouse,
#                 storage_location=storage_location,
#                 batch=batch
#             )

#         except Stock.DoesNotExist:

#             raise ValidationError(
#                 "No stock exists for the selected item and location."
#             )

#         available_quantity = (
#             stock.quantity -
#             stock.reserved_quantity
#         )

#         if quantity > available_quantity:

#             raise ValidationError(
#                 f"Insufficient stock. "
#                 f"Available quantity: {available_quantity}."
#             )

#         previous_quantity = stock.quantity

#         stock.quantity -= quantity

#         stock.save(
#             update_fields=[
#                 "quantity",
#                 "updated_at"
#             ]
#         )

#         movement = StockMovement.objects.create(
#             company=company,
#             plant=plant,
#             item=item,
#             batch=batch,
#             movement_type="issue",
#             quantity=quantity,
#             from_warehouse=warehouse,
#             from_location=storage_location,
#             reference_number=reference_number,
#             remarks=remarks
#         )

#         return {
#             "stock": stock,
#             "movement": movement,
#             "previous_quantity": previous_quantity,
#             "new_quantity": stock.quantity
#         }

#     @staticmethod
#     @transaction.atomic
#     def transfer_stock(
#         *,
#         company,
#         plant,
#         item,
#         from_warehouse,
#         from_location,
#         to_warehouse,
#         to_location,
#         quantity,
#         batch=None,
#         reference_number=None,
#         remarks=None
#     ):

#         quantity = StockService._validate_quantity(
#             quantity
#         )

#         if from_location.id == to_location.id:

#             raise ValidationError(
#                 "Source and destination locations cannot be same."
#             )

#         StockService._validate_item(
#             item,
#             batch
#         )

#         StockService._validate_location(
#             warehouse=from_warehouse,
#             storage_location=from_location
#         )

#         StockService._validate_location(
#             warehouse=to_warehouse,
#             storage_location=to_location
#         )

#         try:

#             source_stock = (
#                 Stock.objects
#                 .select_for_update()
#                 .get(
#                     company=company,
#                     plant=plant,
#                     item=item,
#                     warehouse=from_warehouse,
#                     storage_location=from_location,
#                     batch=batch
#                 )
#             )

#         except Stock.DoesNotExist:

#             raise ValidationError(
#                 "Source stock does not exist."
#             )

#         available_quantity = (
#             source_stock.quantity -
#             source_stock.reserved_quantity
#         )

#         if quantity > available_quantity:

#             raise ValidationError(
#                 f"Insufficient stock. "
#                 f"Available quantity: {available_quantity}."
#             )

#         source_stock.quantity -= quantity

#         source_stock.save(
#             update_fields=[
#                 "quantity",
#                 "updated_at"
#             ]
#         )

#         destination_stock, _ = (
#             Stock.objects
#             .select_for_update()
#             .get_or_create(
#                 company=company,
#                 plant=plant,
#                 item=item,
#                 warehouse=to_warehouse,
#                 storage_location=to_location,
#                 batch=batch,
#                 defaults={
#                     "quantity": Decimal("0"),
#                     "reserved_quantity": Decimal("0")
#                 }
#             )
#         )

#         destination_stock.quantity += quantity

#         destination_stock.save(
#             update_fields=[
#                 "quantity",
#                 "updated_at"
#             ]
#         )

#         movement = StockMovement.objects.create(
#             company=company,
#             plant=plant,
#             item=item,
#             batch=batch,
#             movement_type="transfer",
#             quantity=quantity,
#             from_warehouse=from_warehouse,
#             from_location=from_location,
#             to_warehouse=to_warehouse,
#             to_location=to_location,
#             reference_number=reference_number,
#             remarks=remarks
#         )

#         return {
#             "movement": movement,
#             "source_stock": source_stock,
#             "destination_stock": destination_stock
#         }

#     @staticmethod
#     @transaction.atomic
#     def adjust_stock(
#         *,
#         company,
#         plant,
#         item,
#         warehouse,
#         storage_location,
#         quantity,
#         adjustment_type,
#         batch=None,
#         reference_number=None,
#         remarks=None
#     ):

#         quantity = StockService._validate_quantity(
#             quantity
#         )

#         if adjustment_type not in (
#             "adjustment_in",
#             "adjustment_out"
#         ):

#             raise ValidationError(
#                 "Invalid adjustment type."
#             )

#         if adjustment_type == "adjustment_in":

#             return StockService.receive_stock(
#                 company=company,
#                 plant=plant,
#                 item=item,
#                 warehouse=warehouse,
#                 storage_location=storage_location,
#                 quantity=quantity,
#                 batch=batch,
#                 reference_number=reference_number,
#                 remarks=remarks
#             )

#         return StockService.issue_stock(
#             company=company,
#             plant=plant,
#             item=item,
#             warehouse=warehouse,
#             storage_location=storage_location,
#             quantity=quantity,
#             batch=batch,
#             reference_number=reference_number,
#             remarks=remarks
#         )

#     @staticmethod
#     def get_stock(
#         *,
#         company_id=None,
#         plant_id=None,
#         item_id=None,
#         warehouse_id=None,
#         storage_location_id=None,
#         batch_id=None
#     ):

#         queryset = Stock.objects.select_related(
#             "company",
#             "plant",
#             "item",
#             "warehouse",
#             "storage_location",
#             "batch"
#         )

#         if company_id:
#             queryset = queryset.filter(
#                 company_id=company_id
#             )

#         if plant_id:
#             queryset = queryset.filter(
#                 plant_id=plant_id
#             )

#         if item_id:
#             queryset = queryset.filter(
#                 item_id=item_id
#             )

#         if warehouse_id:
#             queryset = queryset.filter(
#                 warehouse_id=warehouse_id
#             )

#         if storage_location_id:
#             queryset = queryset.filter(
#                 storage_location_id=storage_location_id
#             )

#         if batch_id:
#             queryset = queryset.filter(
#                 batch_id=batch_id
#             )

#         return queryset.order_by(
#             "item__code"
#         )

#     @staticmethod
#     def get_stock_by_id(stock_id):

#         try:

#             return (
#                 Stock.objects
#                 .select_related(
#                     "company",
#                     "plant",
#                     "item",
#                     "warehouse",
#                     "storage_location",
#                     "batch"
#                 )
#                 .get(id=stock_id)
#             )

#         except Stock.DoesNotExist:

#             raise ValidationError(
#                 "Stock record not found."
#             )

#     @staticmethod
#     def list_stock(user=None, company_id=None, plant_id=None, warehouse_id=None, item_id=None):
#         queryset = Stock.objects.select_related(
#             "item",
#             "warehouse",
#             "storage_location",
#             "batch",
#         ).all()

#         # Scope filtering
#         if company_id:
#             queryset = queryset.filter(company_id=company_id)

#         if plant_id:
#             queryset = queryset.filter(plant_id=plant_id)

#         if warehouse_id:
#             queryset = queryset.filter(warehouse_id=warehouse_id)

#         if item_id:
#             queryset = queryset.filter(item_id=item_id)

#         return queryset


from decimal import Decimal

from django.db import transaction
from django.db.models import F, Sum, Q
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.inventory.models.stock import Stock
from apps.inventory.models.stock_movement import StockMovement


class StockService:

    @staticmethod
    def _validate_quantity(quantity):

        quantity = Decimal(str(quantity))

        if quantity <= 0:
            raise ValidationError(
                "Quantity must be greater than zero."
            )

        return quantity

    @staticmethod
    def _validate_item(item, batch=None):

        if not item.is_active:
            raise ValidationError(
                "Item is inactive."
            )

        if item.is_batch_required and batch is None:
            raise ValidationError(
                "Batch is required for this item."
            )

        if batch:

            if batch.item_id != item.id:
                raise ValidationError(
                    "Batch does not belong to selected item."
                )

            if not batch.is_active:
                raise ValidationError(
                    "Batch is inactive."
                )

    @staticmethod
    def _validate_location(
        *,
        warehouse,
        storage_location
    ):

        if not warehouse.is_active:
            raise ValidationError(
                "Warehouse is inactive."
            )

        if not storage_location.is_active:
            raise ValidationError(
                "Storage location is inactive."
            )

        if storage_location.warehouse_id != warehouse.id:
            raise ValidationError(
                "Storage location does not belong to warehouse."
            )

    # =========================================================
    # RECEIVE
    # =========================================================

    @staticmethod
    @transaction.atomic
    def receive_stock(
        *,
        company,
        plant,
        item,
        warehouse,
        storage_location,
        quantity,
        batch=None,
        reference_number=None,
        remarks=None
    ):

        quantity = StockService._validate_quantity(quantity)

        StockService._validate_item(item, batch)

        StockService._validate_location(
            warehouse=warehouse,
            storage_location=storage_location
        )

        stock, _ = Stock.objects.select_for_update().get_or_create(
            company=company,
            plant=plant,
            item=item,
            warehouse=warehouse,
            storage_location=storage_location,
            batch=batch,
            defaults={
                "quantity": Decimal("0"),
                "reserved_quantity": Decimal("0")
            }
        )

        previous_quantity = stock.quantity

        stock.quantity = F("quantity") + quantity

        stock.save(
            update_fields=[
                "quantity",
                "updated_at"
            ]
        )

        stock.refresh_from_db()

        movement = StockMovement.objects.create(
            company=company,
            plant=plant,
            item=item,
            batch=batch,
            movement_type="receipt",
            quantity=quantity,
            to_warehouse=warehouse,
            to_location=storage_location,
            reference_number=reference_number,
            remarks=remarks
        )

        return {
            "stock": stock,
            "movement": movement,
            "previous_quantity": previous_quantity,
            "new_quantity": stock.quantity
        }

    # =========================================================
    # ISSUE
    # =========================================================

    @staticmethod
    @transaction.atomic
    def issue_stock(
        *,
        company,
        plant,
        item,
        warehouse,
        storage_location,
        quantity,
        batch=None,
        reference_number=None,
        remarks=None
    ):

        quantity = StockService._validate_quantity(quantity)

        StockService._validate_item(item, batch)

        StockService._validate_location(
            warehouse=warehouse,
            storage_location=storage_location
        )

        try:

            stock = (
                Stock.objects
                .select_for_update()
                .get(
                    company=company,
                    plant=plant,
                    item=item,
                    warehouse=warehouse,
                    storage_location=storage_location,
                    batch=batch
                )
            )

        except Stock.DoesNotExist:

            raise ValidationError(
                "No stock exists for the selected item and location."
            )

        available_quantity = (
            stock.quantity -
            stock.reserved_quantity
        )

        if quantity > available_quantity:

            raise ValidationError(
                f"Insufficient stock. "
                f"Available quantity: {available_quantity}."
            )

        previous_quantity = stock.quantity

        stock.quantity -= quantity

        stock.save(
            update_fields=[
                "quantity",
                "updated_at"
            ]
        )

        movement = StockMovement.objects.create(
            company=company,
            plant=plant,
            item=item,
            batch=batch,
            movement_type="issue",
            quantity=quantity,
            from_warehouse=warehouse,
            from_location=storage_location,
            reference_number=reference_number,
            remarks=remarks
        )

        return {
            "stock": stock,
            "movement": movement,
            "previous_quantity": previous_quantity,
            "new_quantity": stock.quantity
        }

    # =========================================================
    # TRANSFER
    # =========================================================

    @staticmethod
    @transaction.atomic
    def transfer_stock(
        *,
        company,
        plant,
        item,
        from_warehouse,
        from_location,
        to_warehouse,
        to_location,
        quantity,
        batch=None,
        reference_number=None,
        remarks=None
    ):

        quantity = StockService._validate_quantity(quantity)

        if (
            from_warehouse.id == to_warehouse.id
            and from_location.id == to_location.id
        ):
            raise ValidationError(
                "Source and destination cannot be the same."
            )

        StockService._validate_item(item, batch)

        StockService._validate_location(
            warehouse=from_warehouse,
            storage_location=from_location
        )

        StockService._validate_location(
            warehouse=to_warehouse,
            storage_location=to_location
        )

        try:

            source_stock = (
                Stock.objects
                .select_for_update()
                .get(
                    company=company,
                    plant=plant,
                    item=item,
                    warehouse=from_warehouse,
                    storage_location=from_location,
                    batch=batch
                )
            )

        except Stock.DoesNotExist:

            raise ValidationError(
                "Source stock does not exist."
            )

        available_quantity = (
            source_stock.quantity -
            source_stock.reserved_quantity
        )

        if quantity > available_quantity:

            raise ValidationError(
                f"Insufficient stock. "
                f"Available quantity: {available_quantity}."
            )

        source_stock.quantity -= quantity

        source_stock.save(
            update_fields=[
                "quantity",
                "updated_at"
            ]
        )

        destination_stock, _ = (
            Stock.objects
            .select_for_update()
            .get_or_create(
                company=company,
                plant=plant,
                item=item,
                warehouse=to_warehouse,
                storage_location=to_location,
                batch=batch,
                defaults={
                    "quantity": Decimal("0"),
                    "reserved_quantity": Decimal("0")
                }
            )
        )

        destination_stock.quantity += quantity

        destination_stock.save(
            update_fields=[
                "quantity",
                "updated_at"
            ]
        )

        movement = StockMovement.objects.create(
            company=company,
            plant=plant,
            item=item,
            batch=batch,
            movement_type="transfer",
            quantity=quantity,
            from_warehouse=from_warehouse,
            from_location=from_location,
            to_warehouse=to_warehouse,
            to_location=to_location,
            reference_number=reference_number,
            remarks=remarks
        )

        return {
            "movement": movement,
            "source_stock": source_stock,
            "destination_stock": destination_stock
        }

    # =========================================================
    # ADJUSTMENT
    # =========================================================

    @staticmethod
    @transaction.atomic
    def adjust_stock(
        *,
        company,
        plant,
        item,
        warehouse,
        storage_location,
        quantity,
        adjustment_type,
        batch=None,
        reference_number=None,
        remarks=None
    ):

        if adjustment_type not in (
            "adjustment_in",
            "adjustment_out"
        ):
            raise ValidationError(
                "Invalid adjustment type."
            )

        if adjustment_type == "adjustment_in":

            result = StockService.receive_stock(
                company=company,
                plant=plant,
                item=item,
                warehouse=warehouse,
                storage_location=storage_location,
                quantity=quantity,
                batch=batch,
                reference_number=reference_number,
                remarks=remarks
            )

            result["movement"].movement_type = "adjustment"
            result["movement"].save(
                update_fields=["movement_type"]
            )

            return result

        result = StockService.issue_stock(
            company=company,
            plant=plant,
            item=item,
            warehouse=warehouse,
            storage_location=storage_location,
            quantity=quantity,
            batch=batch,
            reference_number=reference_number,
            remarks=remarks
        )

        result["movement"].movement_type = "adjustment"
        result["movement"].save(
            update_fields=["movement_type"]
        )

        return result

    # =========================================================
    # STOCK LIST
    # =========================================================

    @staticmethod
    def list_stock(
        *,
        company_id=None,
        plant_id=None,
        warehouse_id=None,
        storage_location_id=None,
        category_id=None,
        item_id=None,
        batch_id=None
    ):

        queryset = (
            Stock.objects
            .select_related(
                "company",
                "plant",
                "item",
                "warehouse",
                "storage_location",
                "batch"
            )
        )

        if company_id:
            queryset = queryset.filter(
                company_id=company_id
            )

        if plant_id:
            queryset = queryset.filter(
                plant_id=plant_id
            )

        if warehouse_id:
            queryset = queryset.filter(
                warehouse_id=warehouse_id
            )

        if storage_location_id:
            queryset = queryset.filter(
                storage_location_id=storage_location_id
            )

        if category_id:
            queryset = queryset.filter(
                item__category_id=category_id
            )

        if item_id:
            queryset = queryset.filter(
                item_id=item_id
            )

        if batch_id:
            queryset = queryset.filter(
                batch_id=batch_id
            )

        return queryset.order_by(
            "item__code",
            "warehouse_id"
        )

    # =========================================================
    # GET SINGLE STOCK
    # =========================================================

    @staticmethod
    def get_stock_by_id(stock_id):

        try:

            return (
                Stock.objects
                .select_related(
                    "company",
                    "plant",
                    "item",
                    "warehouse",
                    "storage_location",
                    "batch"
                )
                .get(id=stock_id)
            )

        except Stock.DoesNotExist:

            raise ValidationError(
                "Stock record not found."
            )

    # =========================================================
    # DELETE
    # =========================================================

    @staticmethod
    @transaction.atomic
    def delete_stock(stock):

        if stock.reserved_quantity > 0:

            raise ValidationError(
                "Cannot delete stock with reserved quantity."
            )

        if stock.quantity != 0:

            raise ValidationError(
                "Cannot delete stock while quantity is greater than zero."
            )

        stock.delete()

    # =========================================================
    # STOCK SUMMARY
    # =========================================================

    @staticmethod
    def stock_summary(
        *,
        company_id=None,
        plant_id=None,
        warehouse_id=None
    ):

        queryset = Stock.objects.all()

        if company_id:
            queryset = queryset.filter(
                company_id=company_id
            )

        if plant_id:
            queryset = queryset.filter(
                plant_id=plant_id
            )

        if warehouse_id:
            queryset = queryset.filter(
                warehouse_id=warehouse_id
            )

        total_quantity = queryset.aggregate(
            total=Sum("quantity")
        )["total"] or Decimal("0")

        total_reserved = queryset.aggregate(
            total=Sum("reserved_quantity")
        )["total"] or Decimal("0")

        total_available = (
            total_quantity -
            total_reserved
        )

        return {
            "total_stock_quantity": total_quantity,
            "total_reserved_quantity": total_reserved,
            "total_available_quantity": total_available,
            "stock_records": queryset.count()
        }

    # =========================================================
    # LOW STOCK
    # =========================================================

    @staticmethod
    def low_stock(
        *,
        company_id=None,
        plant_id=None,
        warehouse_id=None,
        category_id=None
    ):

        queryset = (
            Stock.objects
            .select_related(
                "item",
                "warehouse",
                "storage_location",
                "batch"
            )
        )

        if company_id:
            queryset = queryset.filter(
                company_id=company_id
            )

        if plant_id:
            queryset = queryset.filter(
                plant_id=plant_id
            )

        if warehouse_id:
            queryset = queryset.filter(
                warehouse_id=warehouse_id
            )

        if category_id:
            queryset = queryset.filter(
                item__category_id=category_id
            )

        # Assumes Item has reorder_level.
        queryset = queryset.filter(
            quantity__lte=F("item__reorder_level")
        )

        return queryset.order_by(
            "quantity"
        )

    # =========================================================
    # OUT OF STOCK
    # =========================================================

    @staticmethod
    def out_of_stock(
        *,
        company_id=None,
        plant_id=None,
        warehouse_id=None
    ):

        queryset = Stock.objects.select_related(
            "item",
            "warehouse",
            "storage_location",
            "batch"
        )

        if company_id:
            queryset = queryset.filter(
                company_id=company_id
            )

        if plant_id:
            queryset = queryset.filter(
                plant_id=plant_id
            )

        if warehouse_id:
            queryset = queryset.filter(
                warehouse_id=warehouse_id
            )

        return queryset.filter(
            quantity__lte=0
        )

    # =========================================================
    # EXPIRY
    # =========================================================

    @staticmethod
    def expiry_report(
        *,
        days=30,
        company_id=None,
        plant_id=None,
        warehouse_id=None
    ):

        today = timezone.now().date()
        expiry_limit = today + timezone.timedelta(
            days=int(days)
        )

        queryset = Stock.objects.select_related(
            "item",
            "batch",
            "warehouse",
            "storage_location"
        ).filter(
            batch__expiry_date__isnull=False,
            batch__expiry_date__gte=today,
            batch__expiry_date__lte=expiry_limit,
            quantity__gt=0
        )

        if company_id:
            queryset = queryset.filter(
                company_id=company_id
            )

        if plant_id:
            queryset = queryset.filter(
                plant_id=plant_id
            )

        if warehouse_id:
            queryset = queryset.filter(
                warehouse_id=warehouse_id
            )

        return queryset.order_by(
            "batch__expiry_date"
        )

    # =========================================================
    # VALUATION
    # =========================================================

    @staticmethod
    def valuation(
        *,
        company_id=None,
        plant_id=None,
        warehouse_id=None,
        category_id=None
    ):

        queryset = Stock.objects.select_related(
            "item"
        )

        if company_id:
            queryset = queryset.filter(
                company_id=company_id
            )

        if plant_id:
            queryset = queryset.filter(
                plant_id=plant_id
            )

        if warehouse_id:
            queryset = queryset.filter(
                warehouse_id=warehouse_id
            )

        if category_id:
            queryset = queryset.filter(
                item__category_id=category_id
            )

        # Assumes Item has unit_cost.
        total_value = Decimal("0")

        for stock in queryset:

            unit_cost = (
                getattr(
                    stock.item,
                    "unit_cost",
                    Decimal("0")
                ) or Decimal("0")
            )

            total_value += (
                stock.quantity *
                unit_cost
            )

        return {
            "total_quantity": queryset.aggregate(
                total=Sum("quantity")
            )["total"] or Decimal("0"),
            "total_value": total_value,
            "stock_records": queryset.count()
        }