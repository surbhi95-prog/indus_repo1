# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from apps.inventory.serializers.uom_serializer import UOMSerializer
# from apps.inventory.services.uom_service import UOMService


# class UOMListCreateView(APIView):

#     def get(self, request):

#         queryset = UOMService.list(
#             company_id=request.query_params.get("company"),
#             plant_id=request.query_params.get("plant"),
#             is_active=request.query_params.get("is_active")
#         )

#         serializer = UOMSerializer(
#             queryset,
#             many=True
#         )

#         return Response({
#             "success": True,
#             "count": queryset.count(),
#             "data": serializer.data
#         })

#     def post(self, request):

#         serializer = UOMSerializer(
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         uom = UOMService.create(
#             serializer.validated_data
#         )

#         return Response(
#             {
#                 "success": True,
#                 "message": "UOM created successfully.",
#                 "data": UOMSerializer(uom).data
#             },
#             status=status.HTTP_201_CREATED
#         )


# class UOMDetailView(APIView):

#     def get(self, request, uom_id):

#         uom = UOMService.get_by_id(
#             uom_id
#         )

#         return Response({
#             "success": True,
#             "data": UOMSerializer(uom).data
#         })

#     def put(self, request, uom_id):

#         uom = UOMService.get_by_id(
#             uom_id
#         )

#         serializer = UOMSerializer(
#             uom,
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         uom = UOMService.update(
#             uom,
#             serializer.validated_data
#         )

#         return Response({
#             "success": True,
#             "message": "UOM updated successfully.",
#             "data": UOMSerializer(uom).data
#         })

#     def patch(self, request, uom_id):

#         uom = UOMService.get_by_id(
#             uom_id
#         )

#         serializer = UOMSerializer(
#             uom,
#             data=request.data,
#             partial=True
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         uom = UOMService.update(
#             uom,
#             serializer.validated_data
#         )

#         return Response({
#             "success": True,
#             "message": "UOM updated successfully.",
#             "data": UOMSerializer(uom).data
#         })

#     def delete(self, request, uom_id):

#         uom = UOMService.get_by_id(
#             uom_id
#         )

#         UOMService.deactivate(uom)

#         return Response({
#             "success": True,
#             "message": "UOM deactivated successfully."
#         })


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.inventory.serializers.uom_serializer import UOMSerializer
from apps.inventory.services.uom_service import UOMService


def parse_boolean(value):

    if value is None:
        return None

    value = value.lower()

    if value in ["true", "1", "yes"]:
        return True

    if value in ["false", "0", "no"]:
        return False

    return None


class UOMListCreateView(APIView):

    def get(self, request):

        is_active = parse_boolean(
            request.query_params.get("is_active")
        )

        queryset = UOMService.list(
            company_id=request.query_params.get("company"),
            plant_id=request.query_params.get("plant"),
            is_active=is_active
        )

        serializer = UOMSerializer(
            queryset,
            many=True
        )

        return Response({
            "success": True,
            "count": queryset.count(),
            "data": serializer.data
        })

    def post(self, request):

        serializer = UOMSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        uom = UOMService.create(
            serializer.validated_data
        )

        return Response(
            {
                "success": True,
                "message": "UOM created successfully.",
                "data": UOMSerializer(uom).data
            },
            status=status.HTTP_201_CREATED
        )


class UOMDetailView(APIView):

    def get(self, request, uom_id):

        uom = UOMService.get_by_id(
            uom_id
        )

        return Response({
            "success": True,
            "data": UOMSerializer(uom).data
        })

    def put(self, request, uom_id):

        uom = UOMService.get_by_id(
            uom_id
        )

        serializer = UOMSerializer(
            uom,
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        uom = UOMService.update(
            uom,
            serializer.validated_data
        )

        return Response({
            "success": True,
            "message": "UOM updated successfully.",
            "data": UOMSerializer(uom).data
        })

    def patch(self, request, uom_id):

        uom = UOMService.get_by_id(
            uom_id
        )

        serializer = UOMSerializer(
            uom,
            data=request.data,
            partial=True
        )

        serializer.is_valid(
            raise_exception=True
        )

        uom = UOMService.update(
            uom,
            serializer.validated_data
        )

        return Response({
            "success": True,
            "message": "UOM partially updated successfully.",
            "data": UOMSerializer(uom).data
        })

    def delete(self, request, uom_id):

        uom = UOMService.get_by_id(
            uom_id
        )

        UOMService.deactivate(
            uom
        )

        return Response({
            "success": True,
            "message": "UOM deactivated successfully."
        }, status=status.HTTP_200_OK)