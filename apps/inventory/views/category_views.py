# views/category_view.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.inventory.serializers.category_serializer import CategorySerializer
from apps.inventory.services.category_service import CategoryService


def parse_boolean(value):
    if value is None:
        return None

    value = value.lower()

    if value in ["true", "1", "yes"]:
        return True

    if value in ["false", "0", "no"]:
        return False

    return None


class CategoryListCreateView(APIView):

    def get(self, request):

        is_active = parse_boolean(
            request.query_params.get("is_active")
        )

        queryset = CategoryService.list(
            company_id=request.query_params.get("company"),
            plant_id=request.query_params.get("plant"),
            is_active=is_active,
        )

        serializer = CategorySerializer(
            queryset,
            many=True
        )

        return Response({
            "success": True,
            "count": queryset.count(),
            "data": serializer.data
        })

    def post(self, request):

        serializer = CategorySerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        category = CategoryService.create(
            serializer.validated_data
        )

        return Response(
            {
                "success": True,
                "message": "Category created successfully.",
                "data": CategorySerializer(category).data
            },
            status=status.HTTP_201_CREATED
        )


class CategoryDetailView(APIView):

    def get(self, request, category_id):

        category = CategoryService.get_by_id(
            category_id
        )

        return Response({
            "success": True,
            "data": CategorySerializer(category).data
        })

    def put(self, request, category_id):

        category = CategoryService.get_by_id(
            category_id
        )

        serializer = CategorySerializer(
            category,
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        category = CategoryService.update(
            category,
            serializer.validated_data
        )

        return Response({
            "success": True,
            "message": "Category updated successfully.",
            "data": CategorySerializer(category).data
        })

    def patch(self, request, category_id):

        category = CategoryService.get_by_id(
            category_id
        )

        serializer = CategorySerializer(
            category,
            data=request.data,
            partial=True
        )

        serializer.is_valid(
            raise_exception=True
        )

        category = CategoryService.update(
            category,
            serializer.validated_data
        )

        return Response({
            "success": True,
            "message": "Category partially updated successfully.",
            "data": CategorySerializer(category).data
        })

    def delete(self, request, category_id):

        category = CategoryService.get_by_id(
            category_id
        )

        CategoryService.deactivate(category)

        return Response({
            "success": True,
            "message": "Category deactivated successfully."
        }, status=status.HTTP_200_OK)