import mimetypes
from pathlib import Path, PurePosixPath

from django.core.exceptions import SuspiciousFileOperation
from django.http import FileResponse
from rest_framework import status
from apps.accounts.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.authentication import JWTAuthentication
from apps.hrms.models.employee_document import EmployeeDocument
from apps.hrms.services.user_service import UserService


class EmployeeDocumentJWTAuthentication(JWTAuthentication):
    def authenticate_header(self, request):
        return "Bearer"


class EmployeeDocumentView(APIView):
    authentication_classes = [EmployeeDocumentJWTAuthentication]
    permission_classes = [IsAuthenticated]

    inline_content_types = {
        "application/pdf",
        "image/bmp",
        "image/gif",
        "image/jpeg",
        "image/png",
        "image/webp",
    }

    @staticmethod
    def _can_view(user, employee):
        if UserService.is_super_admin(user):
            return (
                not user.company_id
                or user.company_id == employee.company_id
            )

        if UserService.is_hr(user):
            return bool(
                user.company_id
                and user.plant_id
                and user.company_id == employee.company_id
                and user.plant_id == employee.plant_id
            )

        return False

    @staticmethod
    def _not_found():
        return Response(
            {"success": False, "message": "Document not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    @staticmethod
    def _safe_file_path(document):
        if not document.file or not document.file.name:
            raise FileNotFoundError

        stored_name = document.file.name.replace("\\", "/")
        relative_name = PurePosixPath(stored_name)
        upload_to = document.file.field.upload_to
        document_prefix = PurePosixPath(
            upload_to.split("%", 1)[0].rstrip("/")
        )
        if (
            relative_name.is_absolute()
            or ".." in relative_name.parts
            or not document_prefix.parts
            or relative_name.parts[:len(document_prefix.parts)]
            != document_prefix.parts
        ):
            raise SuspiciousFileOperation

        storage = document.file.storage
        storage_root = Path(storage.location).resolve(strict=True)
        document_root = (
            storage_root.joinpath(*document_prefix.parts)
        ).resolve(strict=True)
        document_root.relative_to(storage_root)

        file_path = Path(storage.path(relative_name.as_posix())).resolve(
            strict=True
        )
        file_path.relative_to(document_root)
        if not file_path.is_file():
            raise FileNotFoundError
        return file_path

    def get(self, request, document_id):
        try:
            document = EmployeeDocument.objects.select_related(
                "employee__company",
                "employee__plant",
            ).get(pk=document_id)
        except EmployeeDocument.DoesNotExist:
            return self._not_found()

        if not self._can_view(request.user, document.employee):
            return Response(
                {
                    "success": False,
                    "message": "You do not have permission to view this document.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            file_path = self._safe_file_path(document)
            file_handle = file_path.open("rb")
        except (
            FileNotFoundError,
            NotADirectoryError,
            OSError,
            SuspiciousFileOperation,
            ValueError,
            NotImplementedError,
        ):
            return self._not_found()

        original_name = document.original_file_name or file_path.name
        safe_filename = Path(
            str(original_name).replace("\\", "/")
        ).name
        safe_filename = "".join(
            character
            for character in safe_filename
            if character.isprintable() and character not in "\r\n"
        ) or "document"

        guessed_type = mimetypes.guess_type(safe_filename)[0]
        inline = guessed_type in self.inline_content_types
        response = FileResponse(
            file_handle,
            content_type=(
                guessed_type if inline else "application/octet-stream"
            ),
            as_attachment=not inline,
            filename=safe_filename,
        )
        response["X-Content-Type-Options"] = "nosniff"
        response["Cache-Control"] = "private, no-store"
        return response
