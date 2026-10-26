# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from apps.inventory.serializers.warehouse_serializer import WarehouseSerializer
# from apps.inventory.services.warehouse_service import WarehouseService


# class WarehouseListCreateView(APIView):

#     def get(self, request):

#         queryset = WarehouseService.list(
#             company_id=request.query_params.get("company"),
#             plant_id=request.query_params.get("plant"),
#             warehouse_type=request.query_params.get("warehouse_type"),
#             is_active=request.query_params.get("is_active")
#         )

#         serializer = WarehouseSerializer(
#             queryset,
#             many=True
#         )

#         return Response({
#             "success": True,
#             "count": queryset.count(),
#             "data": serializer.data
#         })

#     def post(self, request):

#         serializer = WarehouseSerializer(
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         warehouse = WarehouseService.create(
#             serializer.validated_data
#         )

#         return Response(
#             {
#                 "success": True,
#                 "message": "Warehouse created successfully.",
#                 "data": WarehouseSerializer(warehouse).data
#             },
#             status=status.HTTP_201_CREATED
#         )


# class WarehouseDetailView(APIView):

#     def get(self, request, warehouse_id):

#         warehouse = WarehouseService.get_by_id(
#             warehouse_id
#         )

#         return Response({
#             "success": True,
#             "data": WarehouseSerializer(warehouse).data
#         })

#     def put(self, request, warehouse_id):

#         warehouse = WarehouseService.get_by_id(
#             warehouse_id
#         )

#         serializer = WarehouseSerializer(
#             warehouse,
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         warehouse = WarehouseService.update(
#             warehouse,
#             serializer.validated_data
#         )

#         return Response({
#             "success": True,
#             "message": "Warehouse updated successfully.",
#             "data": WarehouseSerializer(warehouse).data
#         })

#     def patch(self, request, warehouse_id):

#         warehouse = WarehouseService.get_by_id(
#             warehouse_id
#         )

#         serializer = WarehouseSerializer(
#             warehouse,
#             data=request.data,
#             partial=True
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         warehouse = WarehouseService.update(
#             warehouse,
#             serializer.validated_data
#         )

#         return Response({
#             "success": True,
#             "message": "Warehouse updated successfully.",
#             "data": WarehouseSerializer(warehouse).data
#         })

#     def delete(self, request, warehouse_id):

#         warehouse = WarehouseService.get_by_id(
#             warehouse_id
#         )

#         WarehouseService.deactivate(
#             warehouse
#         )

#         return Response({
#             "success": True,
#             "message": "Warehouse deactivated successfully."
#         })


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.inventory.serializers.warehouse_serializer import (
    WarehouseSerializer
)
from apps.inventory.services.warehouse_service import (
    WarehouseService
)


def parse_boolean(value):

    if value is None:
        return None

    value = value.lower()

    if value in ["true", "1", "yes"]:
        return True

    if value in ["false", "0", "no"]:
        return False

    return None


class WarehouseListCreateView(APIView):

    def get(self, request):

        is_active = parse_boolean(
            request.query_params.get("is_active")
        )

        queryset = WarehouseService.list(
            company_id=request.query_params.get(
                "company"
            ),

            plant_id=request.query_params.get(
                "plant"
            ),

            warehouse_type=request.query_params.get(
                "warehouse_type"
            ),

            is_active=is_active
        )

        serializer = WarehouseSerializer(
            queryset,
            many=True
        )

        return Response({
            "success": True,
            "count": queryset.count(),
            "data": serializer.data
        })

    def post(self, request):

        serializer = WarehouseSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        warehouse = WarehouseService.create(
            serializer.validated_data
        )

        return Response(
            {
                "success": True,
                "message": "Warehouse created successfully.",
                "data": WarehouseSerializer(warehouse).data
            },
            status=status.HTTP_201_CREATED
        )

class WarehouseDetailView(APIView):

    def get(self, request, warehouse_id):

        warehouse = WarehouseService.get_by_id(
            warehouse_id
        )

        return Response({
            "success": True,
            "data": WarehouseSerializer(warehouse).data
        })

    def put(self, request, warehouse_id):

        warehouse = WarehouseService.get_by_id(
            warehouse_id
        )

        serializer = WarehouseSerializer(
            warehouse,
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        warehouse = WarehouseService.update(
            warehouse,
            serializer.validated_data
        )

        return Response({
            "success": True,
            "message": "Warehouse updated successfully.",
            "data": WarehouseSerializer(warehouse).data
        })

    def patch(self, request, warehouse_id):

        warehouse = WarehouseService.get_by_id(
            warehouse_id
        )

        serializer = WarehouseSerializer(
            warehouse,
            data=request.data,
            partial=True
        )

        serializer.is_valid(
            raise_exception=True
        )

        warehouse = WarehouseService.update(
            warehouse,
            serializer.validated_data
        )

        return Response({
            "success": True,
            "message": "Warehouse partially updated successfully.",
            "data": WarehouseSerializer(warehouse).data
        })

    def delete(self, request, warehouse_id):

        warehouse = WarehouseService.get_by_id(
            warehouse_id
        )

        WarehouseService.deactivate(
            warehouse
        )

        return Response({
            "success": True,
            "message": "Warehouse deactivated successfully."
        })