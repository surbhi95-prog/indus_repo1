from rest_framework import status
from apps.accounts.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.authentication import JWTAuthentication

# from apps.masters.permissions.company_permission import (
#     IsSuperAdmin,
#     IsSuperAdminOrCompanyAdmin,
# )
from apps.masters.serializers.company_serializer import (
    CompanyCreateSerializer,
    CompanyListSerializer,
    CompanyDetailSerializer,
    CompanyDetailSerializer,
    CompanyUpdateSerializer,
    
)
from apps.masters.services.company_service import CompanyService
class CompanyListCreateView(APIView):

    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated, IsSuperAdmin]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = CompanyCreateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        company = CompanyService.create_company(
            serializer.validated_data
        )

        return Response(
            {
                "message": "Company created successfully.",
                "data": CompanyDetailSerializer(company).data
            },
            status=status.HTTP_201_CREATED
        )

    def get(self, request):

        companies = CompanyService.get_companies()

        serializer = CompanyListSerializer(
            companies,
            many=True
        )

        return Response(
            {
                "count": companies.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )





class CompanyDetailView(APIView):
    """
    GET    -> Company Details
    PUT    -> Update Company
    PATCH  -> Partial Update Company
    DELETE -> Soft Delete Company
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # ---------------------------------
    # GET Company
    # ---------------------------------

    def get(self, request, company_id):

        company = CompanyService.get_company(company_id)

        # permission = IsSuperAdminOrCompanyAdmin()

        # if not permission.has_object_permission(
        #     request,
        #     self,
        #     company
        # ):
        #     return Response(
        #         {
        #             "message": permission.message
        #         },
        #         status=status.HTTP_403_FORBIDDEN
        #     )

        serializer = CompanyDetailSerializer(company)

        return Response(
            {
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    # ---------------------------------
    # UPDATE Company
    # ---------------------------------

    def put(self, request, company_id):

        # permission = IsSuperAdmin()

        # if not permission.has_permission(request, self):
        #     return Response(
        #         {
        #             "message": permission.message
        #         },
        #         status=status.HTTP_403_FORBIDDEN
        #     )

        company = CompanyService.get_company(company_id)

        serializer = CompanyUpdateSerializer(
            company,
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        company = CompanyService.update_company(
            company,
            serializer.validated_data
        )

        return Response(
            {
                "message": "Company updated successfully.",
                "data": CompanyDetailSerializer(company).data
            },
            status=status.HTTP_200_OK
        )

    # ---------------------------------
    # PARTIAL UPDATE
    # ---------------------------------

    def patch(self, request, company_id):

        # permission = IsSuperAdmin()

        # if not permission.has_permission(request, self):
        #     return Response(
        #         {
        #             "message": permission.message
        #         },
        #         status=status.HTTP_403_FORBIDDEN
        #     )

        company = CompanyService.get_company(company_id)

        serializer = CompanyUpdateSerializer(
            company,
            data=request.data,
            partial=True
        )

        serializer.is_valid(
            raise_exception=True
        )

        company = CompanyService.update_company(
            company,
            serializer.validated_data
        )

        return Response(
            {
                "message": "Company updated successfully.",
                "data": CompanyDetailSerializer(company).data
            },
            status=status.HTTP_200_OK
        )

    # ---------------------------------
    # DELETE Company
    # ---------------------------------

    def delete(self, request, company_id):

        # permission = IsSuperAdmin()

        # if not permission.has_permission(request, self):
        #     return Response(
        #         {
        #             "message": permission.message
        #         },
        #         status=status.HTTP_403_FORBIDDEN
        #     )

        company = CompanyService.get_company(company_id)

        CompanyService.delete_company(company)

        return Response(
            {
                "message": "Company deleted successfully."
            },
            status=status.HTTP_200_OK
        )