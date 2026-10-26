from rest_framework.response import Response
from rest_framework.views import APIView

from apps.inventory.serializers.stock_serializer import (
    StockSerializer
)

from apps.inventory.services.stock_service import (
    StockService
)


# ============================================================
# STOCK SUMMARY
# ============================================================

class StockSummaryReportView(APIView):

    def get(self, request):

        data = StockService.stock_summary(

            company_id=request.query_params.get(
                "company"
            ),

            plant_id=request.query_params.get(
                "plant"
            ),

            warehouse_id=request.query_params.get(
                "warehouse"
            )
        )

        return Response({

            "success": True,

            "data": data

        })


# ============================================================
# STOCK REPORT
# ============================================================

class StockReportView(APIView):

    def get(self, request):

        queryset = StockService.list_stock(

            company_id=request.query_params.get(
                "company"
            ),

            plant_id=request.query_params.get(
                "plant"
            ),

            warehouse_id=request.query_params.get(
                "warehouse"
            ),

            storage_location_id=request.query_params.get(
                "storage_location"
            ),

            category_id=request.query_params.get(
                "category"
            ),

            item_id=request.query_params.get(
                "item"
            ),

            batch_id=request.query_params.get(
                "batch"
            )
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


# ============================================================
# LOW STOCK
# ============================================================

class LowStockReportView(APIView):

    def get(self, request):

        queryset = StockService.low_stock(

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
            )
        )

        serializer = StockSerializer(

            queryset,

            many=True
        )

        return Response({

            "success": True,

            "count": queryset.count(),

            "data": serializer.data

        })


# ============================================================
# OUT OF STOCK
# ============================================================

class OutOfStockReportView(APIView):

    def get(self, request):

        queryset = StockService.out_of_stock(

            company_id=request.query_params.get(
                "company"
            ),

            plant_id=request.query_params.get(
                "plant"
            ),

            warehouse_id=request.query_params.get(
                "warehouse"
            )
        )

        serializer = StockSerializer(

            queryset,

            many=True
        )

        return Response({

            "success": True,

            "count": queryset.count(),

            "data": serializer.data

        })


# ============================================================
# EXPIRY
# ============================================================

class ExpiryReportView(APIView):

    def get(self, request):

        days = int(
            request.query_params.get(
                "days",
                30
            )
        )

        queryset = StockService.expiry_report(

            days=days,

            company_id=request.query_params.get(
                "company"
            ),

            plant_id=request.query_params.get(
                "plant"
            ),

            warehouse_id=request.query_params.get(
                "warehouse"
            )
        )

        serializer = StockSerializer(

            queryset,

            many=True
        )

        return Response({

            "success": True,

            "days": days,

            "count": queryset.count(),

            "data": serializer.data

        })


# ============================================================
# VALUATION
# ============================================================

class ValuationReportView(APIView):

    def get(self, request):

        data = StockService.valuation(

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
            )
        )

        return Response({

            "success": True,

            "data": data

        })


# ============================================================
# DASHBOARD
# ============================================================

class InventoryDashboardView(APIView):

    def get(self, request):

        company = request.query_params.get(
            "company"
        )

        plant = request.query_params.get(
            "plant"
        )

        warehouse = request.query_params.get(
            "warehouse"
        )

        summary = StockService.stock_summary(

            company_id=company,

            plant_id=plant,

            warehouse_id=warehouse
        )

        low_stock = StockService.low_stock(

            company_id=company,

            plant_id=plant,

            warehouse_id=warehouse
        )

        out_of_stock = StockService.out_of_stock(

            company_id=company,

            plant_id=plant,

            warehouse_id=warehouse
        )

        expiry = StockService.expiry_report(

            days=30,

            company_id=company,

            plant_id=plant,

            warehouse_id=warehouse
        )

        return Response({

            "success": True,

            "data": {

                "summary": summary,

                "low_stock_count":
                    low_stock.count(),

                "out_of_stock_count":
                    out_of_stock.count(),

                "expiring_within_30_days":
                    expiry.count()
            }

        })