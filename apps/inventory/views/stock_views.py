# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# from apps.inventory.services.stock_service import StockService
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from apps.inventory.serializers.stock_operation_serializer import (
#     ReceiveStockSerializer
# )
# from apps.inventory.services.stock_service import StockService

# from apps.inventory.serializers.stock_serializer import StockSerializer


# class StockListView(APIView):

#     def get(self, request):
#         try:
#             stocks = StockService.list_stock(
#                 user=request.user,
#                 company_id=request.query_params.get("company"),
#                 plant_id=request.query_params.get("plant"),
#                 item_id=request.query_params.get("item"),
#                 warehouse_id=request.query_params.get("warehouse"),
#             )

#             serializer = StockSerializer(
#                 stocks,
#                 many=True,
#                 context={"request": request}
#             )

#             return Response({
#                 "success": True,
#                 "message": "Stock fetched successfully",
#                 "data": serializer.data,
#             }, status=status.HTTP_200_OK)

#         except Exception as e:
#             return Response({
#                 "success": False,
#                 "message": str(e),
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.inventory.serializers.stock_serializer import (
    StockSerializer
)

from apps.inventory.serializers.stock_operation_serializer import (
    ReceiveStockSerializer,
    IssueStockSerializer,
    TransferStockSerializer,
    AdjustmentSerializer,
    ReturnStockSerializer,
)
from apps.inventory.serializers.stock_movement_serializer import (
    StockMovementSerializer
)

from apps.inventory.services.stock_service import (
    StockService
)


# ============================================================
# STOCK LIST
# ============================================================

class StockListView(APIView):

    def get(self, request):

        stocks = StockService.list_stock(


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
            ),
        )

        serializer = StockSerializer(

            stocks,

            many=True,

            context={
                "request": request
            }
        )

        return Response({

            "success": True,

            "count": stocks.count(),

            "data": serializer.data

        })


# ============================================================
# STOCK DETAIL
# ============================================================

class StockDetailView(APIView):

    def get(self, request, stock_id):

        stock = StockService.get_stock(
            stock_id
        )

        if hasattr(stock, "id"):

            serializer = StockSerializer(
                stock,
                context={
                    "request": request
                }
            )

            data = serializer.data

        else:

            data = stock

        return Response({

            "success": True,

            "data": data

        })


# ============================================================
# RECEIVE
# ============================================================

# class ReceiveStockView(APIView):

#     def post(self, request):

#         serializer = ReceiveStockSerializer(
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         try:

#             result = StockService.receive_stock(
#                 **serializer.validated_data
#             )

#             return Response(

#                 {
#                     "success": True,

#                     "message":
#                         "Stock received successfully.",

#                     "data": {
#                         "stock_id": str(
#                             result["stock"].id
#                         ),

#                         "movement_id": str(
#                             result["movement"].id
#                         ),

#                         "previous_quantity": str(
#                             result["previous_quantity"]
#                         ),

#                         "new_quantity": str(
#                             result["new_quantity"]
#                         ),
#                     }
#                 },

#                 status=status.HTTP_201_CREATED
#             )

#         except ValueError as e:

#             return Response(

#                 {
#                     "success": False,
#                     "message": str(e)
#                 },

#                 status=status.HTTP_400_BAD_REQUEST
#             )


class ReceiveStockView(APIView):

    def post(self, request):

        serializer = ReceiveStockSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:

            result = StockService.receive_stock(
                **serializer.validated_data
            )

            return Response(
                {
                    "success": True,

                    "message":
                        "Stock received successfully.",

                    "data":
                        serialize_stock_operation_result(
                            result,
                            request
                        )
                },

                status=status.HTTP_201_CREATED
            )

        except ValueError as e:

            return Response(
                {
                    "success": False,
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

# ============================================================
# ISSUE
# ============================================================

# class IssueStockView(APIView):

#     def post(self, request):

#         serializer = IssueStockSerializer(
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         try:

#             result = StockService.issue_stock(
#                 **serializer.validated_data
#             )

#             return Response(

#                 {
#                     "success": True,

#                     "message":
#                         "Stock issued successfully.",

#                     "data": result
#                 },

#                 status=status.HTTP_200_OK
#             )

#         except ValueError as e:

#             return Response(

#                 {
#                     "success": False,
#                     "message": str(e)
#                 },

#                 status=status.HTTP_400_BAD_REQUEST
#             )

class IssueStockView(APIView):

    def post(self, request):

        serializer = IssueStockSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:

            result = StockService.issue_stock(
                **serializer.validated_data
            )

            return Response(
                {
                    "success": True,

                    "message":
                        "Stock issued successfully.",

                    "data":
                        serialize_stock_operation_result(
                            result,
                            request
                        )
                },

                status=status.HTTP_200_OK
            )

        except ValueError as e:

            return Response(
                {
                    "success": False,
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

# ============================================================
# TRANSFER
# ============================================================

# class TransferStockView(APIView):

#     def post(self, request):

#         serializer = TransferStockSerializer(
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         try:

#             result = StockService.transfer_stock(
#                 **serializer.validated_data
#             )

#             return Response(

#                 {
#                     "success": True,

#                     "message":
#                         "Stock transferred successfully.",

#                     "data": result
#                 },

#                 status=status.HTTP_200_OK
#             )

#         except ValueError as e:

#             return Response(

#                 {
#                     "success": False,
#                     "message": str(e)
#                 },

#                 status=status.HTTP_400_BAD_REQUEST
#             )



class TransferStockView(APIView):

    def post(self, request):

        serializer = TransferStockSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:

            result = StockService.transfer_stock(
                **serializer.validated_data
            )

            return Response(
                {
                    "success": True,

                    "message":
                        "Stock transferred successfully.",

                    "data":
                        serialize_stock_operation_result(
                            result,
                            request
                        )
                },

                status=status.HTTP_200_OK
            )

        except ValueError as e:

            return Response(
                {
                    "success": False,
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )


# ============================================================
# ADJUSTMENT
# ============================================================

# class AdjustStockView(APIView):

#     def post(self, request):

#         serializer = AdjustmentSerializer(
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         try:

#             result = StockService.adjust_stock(
#                 **serializer.validated_data
#             )

#             return Response(

#                 {
#                     "success": True,

#                     "message":
#                         "Stock adjusted successfully.",

#                     "data": result
#                 },

#                 status=status.HTTP_200_OK
#             )

#         except ValueError as e:

#             return Response(

#                 {
#                     "success": False,
#                     "message": str(e)
#                 },

#                 status=status.HTTP_400_BAD_REQUEST
#             )



class AdjustStockView(APIView):

    def post(self, request):

        serializer = AdjustmentSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:

            result = StockService.adjust_stock(
                **serializer.validated_data
            )

            return Response(
                {
                    "success": True,

                    "message":
                        "Stock adjusted successfully.",

                    "data":
                        serialize_stock_operation_result(
                            result,
                            request
                        )
                },

                status=status.HTTP_200_OK
            )

        except ValueError as e:

            return Response(
                {
                    "success": False,
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

# ============================================================
# RETURN
# ============================================================

# class ReturnStockView(APIView):

#     def post(self, request):

#         serializer = ReturnStockSerializer(
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         try:

#             result = StockService.return_stock(
#                 **serializer.validated_data
#             )

#             return Response(

#                 {
#                     "success": True,

#                     "message":
#                         "Stock returned successfully.",

#                     "data": result
#                 },

#                 status=status.HTTP_200_OK
#             )

#         except ValueError as e:

#             return Response(

#                 {
#                     "success": False,
#                     "message": str(e)
#                 },

#                 status=status.HTTP_400_BAD_REQUEST
#             )


class ReturnStockView(APIView):

    def post(self, request):

        serializer = ReturnStockSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:

            result = StockService.return_stock(
                **serializer.validated_data
            )

            return Response(
                {
                    "success": True,

                    "message":
                        "Stock returned successfully.",

                    "data":
                        serialize_stock_operation_result(
                            result,
                            request
                        )
                },

                status=status.HTTP_200_OK
            )

        except ValueError as e:


            return Response(
        {
            "success": False,
            "message": str(e)
        },
        status=status.HTTP_400_BAD_REQUEST
    )

def serialize_stock_operation_result(result, request):

    data = {}

    # --------------------------------------------------------
    # SINGLE STOCK
    # --------------------------------------------------------

    if "stock" in result:

        data["stock"] = StockSerializer(
            result["stock"],
            context={
                "request": request
            }
        ).data

    # --------------------------------------------------------
    # SOURCE STOCK
    # --------------------------------------------------------

    if "source_stock" in result:

        data["source_stock"] = StockSerializer(
            result["source_stock"],
            context={
                "request": request
            }
        ).data

    # --------------------------------------------------------
    # DESTINATION STOCK
    # --------------------------------------------------------

    if "destination_stock" in result:

        data["destination_stock"] = StockSerializer(
            result["destination_stock"],
            context={
                "request": request
            }
        ).data

    # --------------------------------------------------------
    # MOVEMENT
    # --------------------------------------------------------

    if "movement" in result:

        data["movement"] = StockMovementSerializer(
            result["movement"],
            context={
                "request": request
            }
        ).data

    # --------------------------------------------------------
    # QUANTITIES
    # --------------------------------------------------------

    if "previous_quantity" in result:

        data["previous_quantity"] = str(
            result["previous_quantity"]
        )

    if "new_quantity" in result:

        data["new_quantity"] = str(
            result["new_quantity"]
        )

    return data