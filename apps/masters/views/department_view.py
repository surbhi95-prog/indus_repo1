# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from apps.masters.serializers.department_serializer import (
#     DepartmentCreateSerializer,
#     DepartmentDetailSerializer,
#     DepartmentListSerializer,
#     DepartmentUpdateSerializer,
# )

# from apps.masters.services.department_service import DepartmentService


# class DepartmentView(APIView):

#     def post(self, request):

#         serializer = DepartmentCreateSerializer(
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         department = DepartmentService.create_department(
#             serializer.validated_data
#         )

#         return Response(
#             {
#                 "message": "Department created successfully.",
#                 "data": DepartmentDetailSerializer(department).data,
#             },
#             status=status.HTTP_201_CREATED,
#         )

#     def get(self, request):

#         departments = DepartmentService.get_all_departments()

#         serializer = DepartmentListSerializer(
#             departments,
#             many=True
#         )

#         return Response(
#             serializer.data
#         )


# class DepartmentDetailView(APIView):

#     def get(self, request, department_id):

#         department = DepartmentService.get_department(
#             department_id
#         )

#         serializer = DepartmentDetailSerializer(
#             department
#         )

#         return Response(
#             serializer.data
#         )

#     def put(self, request, department_id):

#         department = DepartmentService.get_department(
#             department_id
#         )

#         serializer = DepartmentUpdateSerializer(
#             department,
#             data=request.data,
#             partial=True
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         department = DepartmentService.update_department(
#             department,
#             serializer.validated_data
#         )

#         return Response(
#             {
#                 "message": "Department updated successfully.",
#                 "data": DepartmentDetailSerializer(department).data,
#             }
#         )

#     def delete(self, request, department_id):

#         department = DepartmentService.get_department(
#             department_id
#         )

#         DepartmentService.delete_department(
#             department
#         )

#         return Response(
#             {
#                 "message": "Department deleted successfully."
#             },
#             status=status.HTTP_204_NO_CONTENT,
#         )

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.masters.serializers.department_serializer import (
    DepartmentCreateSerializer,
    DepartmentDetailSerializer,
    DepartmentListSerializer,
    DepartmentUpdateSerializer,
)

from apps.masters.services.department_service import (
    DepartmentService
)


class DepartmentView(APIView):

    # =========================================================
    # CREATE
    # =========================================================

    def post(self, request):

        serializer = DepartmentCreateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        department = (
            DepartmentService.create_department(
                serializer.validated_data
            )
        )

        return Response(
            {
                "message": (
                    "Department created successfully."
                ),
                "data": DepartmentDetailSerializer(
                    department
                ).data,
            },
            status=status.HTTP_201_CREATED
        )

    # =========================================================
    # LIST + FILTER
    # =========================================================

    def get(self, request):

        company_id = request.query_params.get(
            "company_id"
        )

        plant_id = request.query_params.get(
            "plant_id"
        )

        departments = (
            DepartmentService.get_all_departments(
                company_id=company_id,
                plant_id=plant_id
            )
        )

        serializer = DepartmentListSerializer(
            departments,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class DepartmentDetailView(APIView):

    # =========================================================
    # GET
    # =========================================================

    def get(
        self,
        request,
        department_id
    ):

        department = (
            DepartmentService.get_department(
                department_id
            )
        )

        serializer = DepartmentDetailSerializer(
            department
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # =========================================================
    # UPDATE
    # =========================================================

    def put(
        self,
        request,
        department_id
    ):

        department = (
            DepartmentService.get_department(
                department_id
            )
        )

        serializer = DepartmentUpdateSerializer(
            department,
            data=request.data,
            partial=True
        )

        serializer.is_valid(
            raise_exception=True
        )

        department = (
            DepartmentService.update_department(
                department,
                serializer.validated_data
            )
        )

        return Response(
            {
                "message": (
                    "Department updated successfully."
                ),
                "data": DepartmentDetailSerializer(
                    department
                ).data,
            },
            status=status.HTTP_200_OK
        )

    # =========================================================
    # DELETE
    # =========================================================

    def delete(
        self,
        request,
        department_id
    ):

        department = (
            DepartmentService.get_department(
                department_id
            )
        )

        DepartmentService.delete_department(
            department
        )

        return Response(
            {
                "message": (
                    "Department deleted successfully."
                )
            },
            status=status.HTTP_200_OK
        )