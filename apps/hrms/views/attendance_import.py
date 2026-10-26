from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
)
from rest_framework.response import Response

from apps.hrms.models.attendance_import import (
    AttendanceImport
)

from apps.hrms.models.attendance_import_row import (
    AttendanceImportRow
)

from apps.hrms.serializers.attendance_import import (
    AttendanceImportSerializer,
    AttendanceImportRowSerializer,
)

from apps.hrms.services.excel_attendance_service import (
    ExcelAttendanceService
)


class AttendanceImportViewSet(
    viewsets.ModelViewSet
):

    queryset = (
        AttendanceImport.objects
        .all()
        .order_by("-created_at")
    )

    serializer_class = AttendanceImportSerializer

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        attendance_import = serializer.save(
            file_name=serializer.validated_data[
                "file"
            ].name,
            uploaded_by=(
                str(request.user)
                if request.user.is_authenticated
                else "system"
            )
        )

        ExcelAttendanceService.process_import(
            attendance_import
        )

        attendance_import.refresh_from_db()

        return Response(
            AttendanceImportSerializer(
                attendance_import
            ).data,
            status=status.HTTP_201_CREATED
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="process"
    )
    def process(self, request, pk=None):

        attendance_import = self.get_object()

        result = (
            ExcelAttendanceService.process_import(
                attendance_import
            )
        )

        return Response(
            AttendanceImportSerializer(
                result
            ).data
        )

    @action(
        detail=True,
        methods=["get"],
        url_path="rows"
    )
    def rows(self, request, pk=None):

        attendance_import = self.get_object()

        rows = AttendanceImportRow.objects.filter(
            attendance_import=attendance_import
        ).order_by("row_number")

        serializer = AttendanceImportRowSerializer(
            rows,
            many=True
        )

        return Response(
            {
                "success": True,
                "data": serializer.data
            }
        )