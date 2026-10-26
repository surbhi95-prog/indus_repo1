# from rest_framework.response import Response
# from rest_framework.views import APIView

# from apps.inventory.serializers.stock_movement_serializer import (
#     StockMovementSerializer
# )

# from apps.inventory.services.stock_movement_service import (
#     StockMovementService
# )


# class StockMovementListView(APIView):

#     def get(self, request):

#         queryset = StockMovementService.list(
#             company_id=request.query_params.get(
#                 "company"
#             ),
#             plant_id=request.query_params.get(
#                 "plant"
#             ),
#             item_id=request.query_params.get(
#                 "item"
#             ),
#             batch_id=request.query_params.get(
#                 "batch"
#             ),
#             movement_type=request.query_params.get(
#                 "movement_type"
#             ),
#             warehouse_id=request.query_params.get(
#                 "warehouse"
#             )
#         )

#         serializer = StockMovementSerializer(
#             queryset,
#             many=True
#         )

#         return Response({
#             "success": True,
#             "count": queryset.count(),
#             "data": serializer.data
#         })


# class StockMovementDetailView(APIView):

#     def get(self, request, movement_id):

#         movement = StockMovementService.get_by_id(
#             movement_id
#         )

#         return Response({
#             "success": True,
#             "data": StockMovementSerializer(
#                 movement
#             ).data
#         })


# class ItemStockHistoryView(APIView):

#     def get(self, request, item_id):

#         queryset = StockMovementService.get_item_history(
#             item_id=item_id,
#             plant_id=request.query_params.get(
#                 "plant"
#             )
#         )

#         serializer = StockMovementSerializer(
#             queryset,
#             many=True
#         )

#         return Response({
#             "success": True,
#             "count": queryset.count(),
#             "data": serializer.data
#         })


# class BatchStockHistoryView(APIView):

#     def get(self, request, batch_id):

#         queryset = StockMovementService.get_batch_history(
#             batch_id
#         )

#         serializer = StockMovementSerializer(
#             queryset,
#             many=True
#         )

#         return Response({
#             "success": True,
#             "count": queryset.count(),
#             "data": serializer.data
#         })

# class StockMovementListView(APIView):

#     def get(self, request):

#         queryset = StockMovementService.list(
#             company_id=request.query_params.get("company"),
#             plant_id=request.query_params.get("plant"),
#             item_id=request.query_params.get("item"),
#             batch_id=request.query_params.get("batch"),
#             movement_type=request.query_params.get(
#                 "movement_type"
#             ),
#             warehouse_id=request.query_params.get(
#                 "warehouse"
#             ),
#             from_date=request.query_params.get(
#                 "from_date"
#             ),
#             to_date=request.query_params.get(
#                 "to_date"
#             )
#         )

#         serializer = StockMovementSerializer(
#             queryset,
#             many=True
#         )

#         return Response({
#             "success": True,
#             "count": queryset.count(),
#             "data": serializer.data
#         })
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.inventory.serializers.stock_movement_serializer import (
    StockMovementSerializer
)

from apps.inventory.services.stock_movement_service import (
    StockMovementService
)


# ============================================================
# STOCK MOVEMENT LIST
# ============================================================

class StockMovementListView(APIView):

    def get(self, request):

        queryset = StockMovementService.list(

            user=request.user,

            company_id=request.query_params.get(
                "company"
            ),

            plant_id=request.query_params.get(
                "plant"
            ),

            item_id=request.query_params.get(
                "item"
            ),

            batch_id=request.query_params.get(
                "batch"
            ),

            movement_type=request.query_params.get(
                "movement_type"
            ),

            warehouse_id=request.query_params.get(
                "warehouse"
            ),

            from_date=request.query_params.get(
                "from_date"
            ),

            to_date=request.query_params.get(
                "to_date"
            ),
        )

        serializer = StockMovementSerializer(
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
# STOCK MOVEMENT DETAIL
# ============================================================

class StockMovementDetailView(APIView):

    def get(self, request, movement_id):

        movement = StockMovementService.get_by_id(
            movement_id
        )

        serializer = StockMovementSerializer(
            movement,
            context={
                "request": request
            }
        )

        return Response({

            "success": True,

            "data": serializer.data

        })


# ============================================================
# ITEM STOCK HISTORY
# ============================================================

class ItemStockHistoryView(APIView):

    def get(self, request, item_id):

        queryset = StockMovementService.get_item_history(

            user=request.user,

            item_id=item_id,

            plant_id=request.query_params.get(
                "plant"
            )

        )

        serializer = StockMovementSerializer(
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
# BATCH STOCK HISTORY
# ============================================================

class BatchStockHistoryView(APIView):

    def get(self, request, batch_id):

        queryset = StockMovementService.get_batch_history(

            user=request.user,

            batch_id=batch_id

        )

        serializer = StockMovementSerializer(
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