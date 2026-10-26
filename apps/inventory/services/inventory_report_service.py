from apps.inventory.models.stock import Stock


class InventoryReportService:

    # ========================================================
    # STOCK SUMMARY
    # ========================================================

    @staticmethod
    def stock_summary(
        company_id=None,
        plant_id=None,
        warehouse_id=None,
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

        total_quantity = 0
        total_reserved = 0
        total_available = 0

        for stock in queryset:

            total_quantity += stock.quantity

            total_reserved += stock.reserved_quantity

            total_available += (
                stock.quantity -
                stock.reserved_quantity
            )

        return {
            "total_stock_records": queryset.count(),

            "total_quantity": str(
                total_quantity
            ),

            "total_reserved_quantity": str(
                total_reserved
            ),

            "total_available_quantity": str(
                total_available
            ),
        }

    # ========================================================
    # STOCK REPORT
    # ========================================================

    @staticmethod
    def stock_report(
        company_id=None,
        plant_id=None,
        warehouse_id=None,
        category_id=None,
        item_id=None,
        batch_id=None,
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

        return queryset