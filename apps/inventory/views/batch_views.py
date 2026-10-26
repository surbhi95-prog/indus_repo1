# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from apps.inventory.serializers.batch_serializer import BatchSerializer
# from apps.inventory.services.batch_service import BatchService


# class BatchListCreateView(APIView):

#     def get(self, request):

#         queryset = BatchService.list(
#             company_id=request.query_params.get("company"),
#             plant_id=request.query_params.get("plant"),
#             item_id=request.query_params.get("item"),
#             is_active=request.query_params.get("is_active")
#         )

#         serializer = BatchSerializer(
#             queryset,
#             many=True
#         )

#         return Response({
#             "success": True,
#             "count": queryset.count(),
#             "data": serializer.data
#         })

#     def post(self, request):

#         serializer = BatchSerializer(
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         batch = BatchService.create(
#             serializer.validated_data
#         )

#         return Response(
#             {
#                 "success": True,
#                 "message": "Batch created successfully.",
#                 "data": BatchSerializer(batch).data
#             },
#             status=status.HTTP_201_CREATED
#         )


# class BatchDetailView(APIView):

#     def get(self, request, batch_id):

#         batch = BatchService.get_by_id(
#             batch_id
#         )

#         return Response({
#             "success": True,
#             "data": BatchSerializer(batch).data
#         })

#     def put(self, request, batch_id):

#         batch = BatchService.get_by_id(
#             batch_id
#         )

#         serializer = BatchSerializer(
#             batch,
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         batch = BatchService.update(
#             batch,
#             serializer.validated_data
#         )

#         return Response({
#             "success": True,
#             "message": "Batch updated successfully.",
#             "data": BatchSerializer(batch).data
#         })

#     def patch(self, request, batch_id):

#         batch = BatchService.get_by_id(
#             batch_id
#         )

#         serializer = BatchSerializer(
#             batch,
#             data=request.data,
#             partial=True
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         batch = BatchService.update(
#             batch,
#             serializer.validated_data
#         )

#         return Response({
#             "success": True,
#             "message": "Batch updated successfully.",
#             "data": BatchSerializer(batch).data
#         })


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.inventory.serializers.batch_serializer import BatchSerializer
from apps.inventory.services.batch_service import BatchService


class BatchListCreateView(APIView):

    def get(self, request):

        queryset = BatchService.list(

            company_id=request.query_params.get(
                "company"
            ),

            plant_id=request.query_params.get(
                "plant"
            ),

            item_id=request.query_params.get(
                "item"
            ),

            is_active=request.query_params.get(
                "is_active"
            ),

            expiry_before=request.query_params.get(
                "expiry_before"
            ),

            search=request.query_params.get(
                "search"
            ),
        )

        serializer = BatchSerializer(
            queryset,
            many=True
        )

        return Response({

            "success": True,

            "count": queryset.count(),

            "data": serializer.data

        })

    def post(self, request):

        serializer = BatchSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        batch = BatchService.create(
            serializer.validated_data
        )

        return Response(

            {
                "success": True,

                "message": "Batch created successfully.",

                "data": BatchSerializer(
                    batch
                ).data
            },

            status=status.HTTP_201_CREATED
        )


class BatchDetailView(APIView):

    def get(self, request, batch_id):

        batch = BatchService.get_by_id(
            batch_id
        )

        return Response({

            "success": True,

            "data": BatchSerializer(
                batch
            ).data

        })

    def put(self, request, batch_id):

        batch = BatchService.get_by_id(
            batch_id
        )

        serializer = BatchSerializer(

            batch,

            data=request.data

        )

        serializer.is_valid(
            raise_exception=True
        )

        batch = BatchService.update(

            batch,

            serializer.validated_data

        )

        return Response({

            "success": True,

            "message": "Batch updated successfully.",

            "data": BatchSerializer(
                batch
            ).data

        })

    def patch(self, request, batch_id):

        batch = BatchService.get_by_id(
            batch_id
        )

        serializer = BatchSerializer(

            batch,

            data=request.data,

            partial=True

        )

        serializer.is_valid(
            raise_exception=True
        )

        batch = BatchService.update(

            batch,

            serializer.validated_data

        )

        return Response({

            "success": True,

            "message": "Batch updated successfully.",

            "data": BatchSerializer(
                batch
            ).data

        })
class BatchDetailView(APIView):

    def get(self, request, batch_id):

        batch = BatchService.get_by_id(
            batch_id
        )

        return Response({
            "success": True,
            "data": BatchSerializer(batch).data
        })

    def put(self, request, batch_id):

        batch = BatchService.get_by_id(
            batch_id
        )

        serializer = BatchSerializer(
            batch,
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        batch = BatchService.update(
            batch,
            serializer.validated_data
        )

        return Response({
            "success": True,
            "message": "Batch updated successfully.",
            "data": BatchSerializer(batch).data
        })

    def patch(self, request, batch_id):

        batch = BatchService.get_by_id(
            batch_id
        )

        serializer = BatchSerializer(
            batch,
            data=request.data,
            partial=True
        )

        serializer.is_valid(
            raise_exception=True
        )

        batch = BatchService.update(
            batch,
            serializer.validated_data
        )

        return Response({
            "success": True,
            "message": "Batch updated successfully.",
            "data": BatchSerializer(batch).data
        })

