from rest_framework.response import Response
from rest_framework.views import APIView

from apps.inventory.services.inventory_report_service import (
    InventoryReportService
)
from apps.inventory.serializers.stock_serializer import (
    StockSerializer
)

# ============================================================
# STOCK SUMMARY
# ============================================================

class StockSummaryReportView(APIView):

    def get(self, request):

        result = InventoryReportService.stock_summary(

            company_id=request.query_params.get(
                "company"
            ),

            plant_id=request.query_params.get(
                "plant"
            ),

            warehouse_id=request.query_params.get(
                "warehouse"
            ),
        )

        return Response({

            "success": True,

            "data": result

        })


# ============================================================
# STOCK REPORT
# ============================================================
class StockReportView(APIView):

    def get(self, request):

        queryset = InventoryReportService.stock_report(

            company_id=request.query_params.get(
                "company"
            ),

            plant_id=request.query_params.get(
                "plant"
            ),

            warehouse_id=request.query_params.get(
                "warehouse"
            ),

            category_id=request.query_params.get(
                "category"
            ),

            item_id=request.query_params.get(
                "item"
            ),

            batch_id=request.query_params.get(
                "batch"
            ),
        )

        serializer = StockSerializer(
            queryset,
            many=True,
            context={
                "request": request
            }
        )

        return Response({

            "success": True,

            "count": queryset.count(),

            "data": serializer.data

        })