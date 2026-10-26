# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from apps.masters.serializers.plant_serializer import (
#     PlantCreateSerializer,
#     PlantDetailSerializer,
#     PlantListSerializer,
#     PlantUpdateSerializer,
# )

# from apps.masters.services.plant_service import PlantService


# class PlantView(APIView):

#     def post(self, request):

#         serializer = PlantCreateSerializer(
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         plant = PlantService.create_plant(
#             serializer.validated_data
#         )

#         return Response(
#             {
#                 "message": "Plant created successfully.",
#                 "data": PlantDetailSerializer(plant).data,
#             },
#             status=status.HTTP_201_CREATED,
#         )

#     def get(self, request):

#         plants = PlantService.get_all_plants()

#         serializer = PlantListSerializer(
#             plants,
#             many=True
#         )

#         return Response(
#             serializer.data
#         )


# class PlantDetailView(APIView):

#     def get(self, request, plant_id):

#         plant = PlantService.get_plant(
#             plant_id
#         )

#         serializer = PlantDetailSerializer(
#             plant
#         )

#         return Response(
#             serializer.data
#         )

#     def put(self, request, plant_id):

#         plant = PlantService.get_plant(
#             plant_id
#         )

#         serializer = PlantUpdateSerializer(
#             plant,
#             data=request.data,
#             partial=True
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         plant = PlantService.update_plant(
#             plant,
#             serializer.validated_data
#         )

#         return Response(
#             {
#                 "message": "Plant updated successfully.",
#                 "data": PlantDetailSerializer(
#                     plant
#                 ).data,
#             }
#         )

#     def delete(self, request, plant_id):

#         plant = PlantService.get_plant(
#             plant_id
#         )

#         PlantService.delete_plant(
#             plant
#         )

#         return Response(
#             {
#                 "message": "Plant deleted successfully."
#             },
#             status=status.HTTP_204_NO_CONTENT,
#         )


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.masters.serializers.plant_serializer import (
    PlantCreateSerializer,
    PlantDetailSerializer,
    PlantDetailsSerializer,
    PlantListSerializer,
    PlantUpdateSerializer,
)

from apps.masters.services.plant_service import (
    PlantService
)


class PlantView(APIView):

    # =========================================================
    # CREATE PLANT
    # =========================================================

    def post(self, request):

        serializer = PlantCreateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        plant = PlantService.create_plant(
            serializer.validated_data
        )

        return Response(
            {
                "message": "Plant created successfully.",
                "data": PlantDetailSerializer(
                    plant
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )

    # =========================================================
    # LIST PLANTS
    # =========================================================

    def get(self, request):

        company_id = request.query_params.get(
            "company_id"
        )

        plants = PlantService.get_all_plants(
            company_id=company_id
        )

        serializer = PlantListSerializer(
            plants,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class PlantDetailView(APIView):

    # =========================================================
    # GET
    # =========================================================

    def get(self, request, plant_id):

        plant = PlantService.get_plant(
            plant_id
        )

        serializer = PlantDetailSerializer(
            plant
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # =========================================================
    # UPDATE
    # =========================================================

    def put(self, request, plant_id):

        plant = PlantService.get_plant(
            plant_id
        )

        serializer = PlantUpdateSerializer(
            plant,
            data=request.data,
            partial=True
        )

        serializer.is_valid(
            raise_exception=True
        )

        plant = PlantService.update_plant(
            plant,
            serializer.validated_data
        )

        return Response(
            {
                "message": "Plant updated successfully.",
                "data": PlantDetailSerializer(
                    plant
                ).data,
            },
            status=status.HTTP_200_OK
        )

    # =========================================================
    # DELETE
    # =========================================================

    def delete(self, request, plant_id):

        plant = PlantService.get_plant(
            plant_id
        )

        PlantService.delete_plant(
            plant
        )

        return Response(
            {
                "message": "Plant deleted successfully."
            },
            status=status.HTTP_200_OK
        )


class PlantDetailsView(APIView):

    def get(self, request, plant_id):
        plant = PlantService.get_plant_details(plant_id)
        serializer = PlantDetailsSerializer(plant)
        return Response(serializer.data, status=status.HTTP_200_OK)
