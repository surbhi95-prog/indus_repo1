# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from apps.inventory.serializers.storage_location_serializer import (
#     StorageLocationSerializer
# )

# from apps.inventory.services.storage_location_service import (
#     StorageLocationService
# )


# class StorageLocationListCreateView(APIView):

#     def get(self, request):

#         queryset = StorageLocationService.list(
#             company_id=request.query_params.get("company"),
#             plant_id=request.query_params.get("plant"),
#             warehouse_id=request.query_params.get("warehouse"),
#             is_active=request.query_params.get("is_active")
#         )

#         serializer = StorageLocationSerializer(
#             queryset,
#             many=True
#         )

#         return Response({
#             "success": True,
#             "count": queryset.count(),
#             "data": serializer.data
#         })

#     def post(self, request):

#         serializer = StorageLocationSerializer(
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         location = StorageLocationService.create(
#             serializer.validated_data
#         )

#         return Response(
#             {
#                 "success": True,
#                 "message": "Storage location created successfully.",
#                 "data": StorageLocationSerializer(location).data
#             },
#             status=status.HTTP_201_CREATED
#         )


# class StorageLocationDetailView(APIView):

#     def get(self, request, location_id):

#         location = StorageLocationService.get_by_id(
#             location_id
#         )

#         return Response({
#             "success": True,
#             "data": StorageLocationSerializer(location).data
#         })

#     def put(self, request, location_id):

#         location = StorageLocationService.get_by_id(
#             location_id
#         )

#         serializer = StorageLocationSerializer(
#             location,
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         location = StorageLocationService.update(
#             location,
#             serializer.validated_data
#         )

#         return Response({
#             "success": True,
#             "message": "Storage location updated successfully.",
#             "data": StorageLocationSerializer(location).data
#         })

#     def patch(self, request, location_id):

#         location = StorageLocationService.get_by_id(
#             location_id
#         )

#         serializer = StorageLocationSerializer(
#             location,
#             data=request.data,
#             partial=True
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         location = StorageLocationService.update(
#             location,
#             serializer.validated_data
#         )

#         return Response({
#             "success": True,
#             "message": "Storage location updated successfully.",
#             "data": StorageLocationSerializer(location).data
#         })

#     def delete(self, request, location_id):

#         location = StorageLocationService.get_by_id(
#             location_id
#         )

#         StorageLocationService.deactivate(
#             location
#         )

#         return Response({
#             "success": True,
#             "message": "Storage location deactivated successfully."
#         })


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.inventory.serializers.storage_location_serializer import (
    StorageLocationSerializer
)

from apps.inventory.services.storage_location_service import (
    StorageLocationService
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


class StorageLocationListCreateView(APIView):

    def get(self, request):

        is_active = parse_boolean(
            request.query_params.get("is_active")
        )

        queryset = StorageLocationService.list(

            company_id=request.query_params.get(
                "company"
            ),

            plant_id=request.query_params.get(
                "plant"
            ),

            warehouse_id=request.query_params.get(
                "warehouse"
            ),

            is_active=is_active
        )

        serializer = StorageLocationSerializer(
            queryset,
            many=True
        )

        return Response({
            "success": True,
            "count": queryset.count(),
            "data": serializer.data
        })

    def post(self, request):

        serializer = StorageLocationSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        location = StorageLocationService.create(
            serializer.validated_data
        )

        return Response(
            {
                "success": True,
                "message":
                    "Storage location created successfully.",
                "data":
                    StorageLocationSerializer(location).data
            },
            status=status.HTTP_201_CREATED
        )

class StorageLocationDetailView(APIView):

    def get(self, request, location_id):

        location = StorageLocationService.get_by_id(
            location_id
        )

        return Response({
            "success": True,
            "data": StorageLocationSerializer(location).data
        })

    def put(self, request, location_id):

        location = StorageLocationService.get_by_id(
            location_id
        )

        serializer = StorageLocationSerializer(
            location,
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        location = StorageLocationService.update(
            location,
            serializer.validated_data
        )

        return Response({
            "success": True,
            "message":
                "Storage location updated successfully.",
            "data":
                StorageLocationSerializer(location).data
        })

    def patch(self, request, location_id):

        location = StorageLocationService.get_by_id(
            location_id
        )

        serializer = StorageLocationSerializer(
            location,
            data=request.data,
            partial=True
        )

        serializer.is_valid(
            raise_exception=True
        )

        location = StorageLocationService.update(
            location,
            serializer.validated_data
        )

        return Response({
            "success": True,
            "message":
                "Storage location partially updated successfully.",
            "data":
                StorageLocationSerializer(location).data
        })

    def delete(self, request, location_id):

        location = StorageLocationService.get_by_id(
            location_id
        )

        StorageLocationService.deactivate(
            location
        )

        return Response({
            "success": True,
            "message":
                "Storage location deactivated successfully."
        })