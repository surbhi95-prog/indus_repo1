from uuid import UUID
from rest_framework import status

from apps.accounts.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.authentication import JWTAuthentication

from apps.hrms.serializers.shift_serializer import (
    ShiftSerializer
)
from apps.hrms.serializers.shift_list_serializer import (
    ShiftListSerializer
)
from apps.hrms.serializers.shift_update_serializer import ShiftUpdateSerializer
from apps.hrms.models.shift import Shift
from apps.hrms.shift_types import normalize_shift_type
from apps.hrms.services.shift_service import (
    ShiftService,
    DuplicateShiftError,
)
from apps.masters.models.company import Company
from apps.masters.models.plant import Plant



class ShiftListCreateView(APIView):

    authentication_classes = [
        JWTAuthentication
    ]

    permission_classes = [
        IsAuthenticated
    ]
        # =========================================================
    # GET SHIFTS
    # =========================================================

    def get(self, request):

        try:

            # -------------------------------------------------
            # QUERY PARAMETERS
            # -------------------------------------------------

            company_id = request.query_params.get(
                "company_id"
            )

            plant_id = request.query_params.get(
                "plant_id"
            )

            shift_type = request.query_params.get(
                "shift_type"
            )
            
            # -------------------------------------------------
            # PLANT REQUIRES COMPANY
            # -------------------------------------------------

            if plant_id and not company_id:

                return Response(
                    {
                        "success": False,
                        "message":
                            "company_id is required when "
                            "plant_id is provided."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # -------------------------------------------------
            # VALIDATE COMPANY UUID
            # -------------------------------------------------

            if company_id:

                try:

                    UUID(str(company_id))

                except ValueError:

                    return Response(
                        {
                            "success": False,
                            "message":
                                "Invalid company_id."
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # -------------------------------------------------
            # VALIDATE PLANT UUID
            # -------------------------------------------------

            if plant_id:

                try:

                    UUID(str(plant_id))

                except ValueError:

                    return Response(
                        {
                            "success": False,
                            "message":
                                "Invalid plant_id."
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # -------------------------------------------------
            # VALIDATE COMPANY EXISTS
            # -------------------------------------------------

            if company_id:

                company_exists = (
                    Company.objects
                    .filter(
                        id=company_id
                    )
                    .exists()
                )

                if not company_exists:

                    return Response(
                        {
                            "success": False,
                            "message":
                                "Company not found."
                        },
                        status=status.HTTP_404_NOT_FOUND
                    )

            # -------------------------------------------------
            # VALIDATE PLANT EXISTS
            # -------------------------------------------------

            if plant_id:

                plant = (
                    Plant.objects
                    .filter(
                        id=plant_id
                    )
                    .first()
                )

                if not plant:

                    return Response(
                        {
                            "success": False,
                            "message":
                                "Plant not found."
                        },
                        status=status.HTTP_404_NOT_FOUND
                    )

                # ---------------------------------------------
                # COMPANY -> PLANT VALIDATION
                # ---------------------------------------------

                if plant.company_id != UUID(
                    str(company_id)
                ):

                    return Response(
                        {
                            "success": False,
                            "message":
                                "The selected plant does "
                                "not belong to the selected "
                                "company."
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # -------------------------------------------------
            # VALIDATE SHIFT TYPE
            # -------------------------------------------------

            if shift_type:

                shift_type = normalize_shift_type(shift_type)

                valid_shift_types = [
                    "general",
                    "contract"
                ]

                if shift_type not in valid_shift_types:

                    return Response(
                        {
                            "success": False,
                            "message":
                                "Invalid shift_type. "
                                "Allowed values are "
                                "general and contract."
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # -------------------------------------------------
            # GET SHIFTS
            # -------------------------------------------------

            queryset = ShiftService.get_shifts(
                company_id=company_id,
                plant_id=plant_id,
                shift_type=shift_type
            )

            # -------------------------------------------------
            # SERIALIZE
            # -------------------------------------------------

            serializer = ShiftListSerializer(
                queryset,
                many=True
            )

            # -------------------------------------------------
            # RESPONSE
            # -------------------------------------------------

            return Response(
                {
                    "success": True,
                    "count": queryset.count(),
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        except DuplicateShiftError as exc:

            response_data = {
                "success": False,
                "message": str(exc),
                "errors": {
                    "detail": str(exc)
                }
            }

            # Return the already existing shift
            # so frontend knows which record caused
            # the duplicate conflict.
            if exc.shift:

                response_data["existing_shift"] = (
                    ShiftSerializer(
                        exc.shift
                    ).data
                )

            return Response(
                response_data,
                status=status.HTTP_409_CONFLICT
            )

        except ValueError as exc:

            return Response(
                {
                    "success": False,
                    "message": str(exc),
                    "errors": {
                        "detail": str(exc)
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as exc:

            return Response(
                {
                    "success": False,
                    "message":
                        "Failed to create shift.",
                    "errors": {
                        "detail": str(exc)
                    }
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # =========================================================
    # CREATE SHIFT
    # =========================================================
    
    def post(self, request):

        serializer = ShiftSerializer(
            data=request.data
        )

        if not serializer.is_valid():

            return Response(
                {
                    "success": False,
                    "message":
                        "Shift validation failed.",
                    "errors":
                        serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            shift = ShiftService.create_shift(
                validated_data=
                    serializer.validated_data,
                user=request.user
            )

        except Exception as exc:

            return Response(
                {
                    "success": False,
                    "message":
                        "Failed to create shift.",
                    "errors": {
                        "detail": str(exc)
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "success": True,
                "message":
                    "Shift created successfully.",
                "data":
                    ShiftSerializer(
                        shift
                    ).data
            },
            status=status.HTTP_201_CREATED
        )
