from django.utils import timezone

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.hrms.models.biometric_device import (
    BiometricDevice
)

from apps.hrms.models.biometric_employee import (
    BiometricEmployee
)

from apps.hrms.models.biometric_punch import (
    BiometricPunch
)

from apps.hrms.models.employee import Employee

from apps.hrms.serializers.biometric import (
    BiometricDeviceSerializer,
    BiometricEmployeeSerializer,
    BiometricPunchSerializer,
)

from apps.hrms.services.attendance_service import (
    AttendanceService
)


class BiometricDeviceViewSet(viewsets.ModelViewSet):

    queryset = BiometricDevice.objects.all().order_by(
        "-created_at"
    )

    serializer_class = BiometricDeviceSerializer

    @action(
        detail=True,
        methods=["post"],
        url_path="sync"
    )
    def sync(self, request, pk=None):

        device = self.get_object()

        # ------------------------------------------
        # Actual device integration will be added here
        # ------------------------------------------

        device.last_sync_at = timezone.now()
        device.save(
            update_fields=["last_sync_at"]
        )

        return Response(
            {
                "success": True,
                "message": (
                    "Biometric sync initiated successfully."
                ),
                "device_id": device.id,
                "last_sync_at": device.last_sync_at,
            }
        )


class BiometricEmployeeViewSet(
    viewsets.ModelViewSet
):

    queryset = (
        BiometricEmployee.objects
        .select_related(
            "employee",
            "device"
        )
        .all()
        .order_by("-created_at")
    )

    serializer_class = BiometricEmployeeSerializer


class BiometricPunchViewSet(
    viewsets.ModelViewSet
):

    queryset = (
    BiometricPunch.objects
    .all()
    .order_by("-punch_time")
)

    serializer_class = BiometricPunchSerializer

    def create(self, request, *args, **kwargs):

        device_id = request.data.get(
            "device"
        )

        biometric_user_id = request.data.get(
            "biometric_user_id"
        )

        punch_datetime = request.data.get(
            "punch_datetime"
        )

        punch_type = request.data.get(
            "punch_type",
            "in_time"
        )

        if not device_id:

            return Response(
                {
                    "success": False,
                    "message": "Device is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not biometric_user_id:

            return Response(
                {
                    "success": False,
                    "message": (
                        "biometric_user_id is required."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not punch_datetime:

            return Response(
                {
                    "success": False,
                    "message": (
                        "punch_datetime is required."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            mapping = (
                BiometricEmployee.objects
                .select_related(
                    "employee",
                    "device"
                )
                .get(
                    device_id=device_id,
                    biometric_user_id=biometric_user_id,
                    is_active=True
                )
            )

        except BiometricEmployee.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": (
                        "Biometric employee mapping "
                        "not found."
                    )
                },
                status=status.HTTP_404_NOT_FOUND
            )

        punch = BiometricPunch.objects.create(
            device_id=device_id,
            employee=mapping.employee,
            biometric_user_id=biometric_user_id,
            punch_datetime=punch_datetime,
            punch_type=punch_type,
            raw_data=request.data,
            sync_status="processed"
        )

        attendance = AttendanceService.add_punch(
            employee=mapping.employee,
            punch_time=punch.punch_datetime,
            punch_type=punch_type,
            source="biometric",
            device_id=str(device_id)
        )

        return Response(
            {
                "success": True,
                "message": (
                    "Biometric punch processed successfully."
                ),
                "punch": BiometricPunchSerializer(
                    punch
                ).data,
                "attendance": {
                    "id": attendance.id,
                    "employee": (
                        attendance.employee.employee_code
                    ),
                    "date": attendance.attendance_date,
                    "status": attendance.status,
                }
            },
            status=status.HTTP_201_CREATED
        )