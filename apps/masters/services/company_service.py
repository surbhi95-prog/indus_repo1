# from django.db import transaction
# from django.shortcuts import get_object_or_404

# from rest_framework.exceptions import ValidationError

# from apps.masters.models.company import Company


# class CompanyService:

#     @staticmethod
#     @transaction.atomic
#     def create_company(validated_data):
#         """
#         Create Company
#         """

#         name = validated_data.get("name").strip()

#         code = validated_data.get("code")

#         if code:
#             code = code.strip().upper()

#         # -------------------------
#         # Duplicate Name
#         # -------------------------

#         if Company.objects.filter(
#             name__iexact=name
#         ).exists():

#             raise ValidationError(
#                 {
#                     "name": [
#                         "Company name already exists."
#                     ]
#                 }
#             )

#         # -------------------------
#         # Duplicate Code
#         # -------------------------
#         if code:

#            if Company.objects.filter(
#         code__iexact=code
#          ).exists():

#             raise ValidationError(
#             {
#                 "code": [
#                     f"Company code '{code}' already exists."
#                 ]
#             }
#         )

#         return Company.objects.create(
#             name=name,
#             code=code,
#         )

#     @staticmethod
#     def get_companies():
#         """
#         Fetch all active companies
#         """

#         return Company.objects.filter(
#             is_active=True
#         ).order_by("name")

#     @staticmethod
#     def get_company(company_id):
#         """
#         Fetch single company
#         """

#         return get_object_or_404(
#             Company,
#             id=company_id,
#             is_active=True
#         )

#     @staticmethod
#     @transaction.atomic
#     def update_company(company, validated_data):
#         """
#         Update Company
#         """

#         name = validated_data.get(
#             "name",
#             company.name
#         ).strip()

#         code = validated_data.get(
#             "code",
#             company.code
#         )

#         if code:
#             code = code.strip().upper()

#         # -------------------------
#         # Duplicate Name
#         # -------------------------

#         if Company.objects.filter(
#             name__iexact=name
#         ).exclude(
#             id=company.id
#         ).exists():

#             raise ValidationError(
#                 {
#                     "name": [
#                         "Company name already exists."
#                     ]
#                 }
#             )

#         # -------------------------
#         # Duplicate Code
#         # -------------------------
#          # Duplicate Code

#         if code:

#            if Company.objects.filter(
#         code__iexact=code
#     ).exclude(
#         id=company.id
#     ).exists():

#             raise ValidationError(
#             {
#                 "code": [
#                     f"Company code '{code}' already exists."
#                 ]
#             }
#         )
        
#         company.name = name
#         company.code = code
#         company.is_active = validated_data.get(
#             "is_active",
#             company.is_active
#         )

#         company.save()

#         return company

#     @staticmethod
#     @transaction.atomic
#     def delete_company(company):
#         """
#         Soft Delete Company
#         """

#         company.is_active = False
#         company.save()

#         return company



from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework.exceptions import ValidationError

from apps.masters.models.company import Company


class CompanyService:

    # =========================================================
    # CREATE
    # =========================================================

    @staticmethod
    @transaction.atomic
    def create_company(validated_data):

        # -----------------------------------------------------
        # EXTRACT ADDRESS
        # -----------------------------------------------------

        address_data = validated_data.pop(
            "address",
            {}
        )

        # -----------------------------------------------------
        # NAME
        # -----------------------------------------------------

        name = validated_data.get(
            "name",
            ""
        ).strip()

        # -----------------------------------------------------
        # CODE
        # -----------------------------------------------------

        code = validated_data.get(
            "code"
        )

        if code:
            code = code.strip().upper()

        # -----------------------------------------------------
        # DUPLICATE NAME
        # -----------------------------------------------------

        if Company.objects.filter(
            name__iexact=name
        ).exists():

            raise ValidationError(
                {
                    "name": [
                        "Company name already exists."
                    ]
                }
            )

        # -----------------------------------------------------
        # DUPLICATE CODE
        # -----------------------------------------------------

        if code and Company.objects.filter(
            code__iexact=code
        ).exists():

            raise ValidationError(
                {
                    "code": [
                        f"Company code '{code}' already exists."
                    ]
                }
            )

        # -----------------------------------------------------
        # REMOVE NAME & CODE
        # -----------------------------------------------------

        validated_data.pop("name", None)
        validated_data.pop("code", None)

        # -----------------------------------------------------
        # CREATE COMPANY
        # -----------------------------------------------------

        company = Company.objects.create(
            name=name,
            code=code,
            **validated_data,
            **address_data
        )

        return company

    # =========================================================
    # LIST
    # =========================================================

    @staticmethod
    def get_companies():

        return Company.objects.filter(
            is_active=True
        ).order_by("name")

    # =========================================================
    # DETAIL
    # =========================================================

    @staticmethod
    def get_company(company_id):

        return get_object_or_404(
            Company,
            id=company_id,
            is_active=True
        )

    # =========================================================
    # UPDATE
    # =========================================================

    @staticmethod
    @transaction.atomic
    def update_company(company, validated_data):

        address_data = validated_data.pop(
            "address",
            None
        )

        name = validated_data.get(
            "name",
            company.name
        ).strip()

        code = validated_data.get(
            "code",
            company.code
        )

        if code:
            code = code.strip().upper()

        # -----------------------------------------------------
        # DUPLICATE NAME
        # -----------------------------------------------------

        if Company.objects.filter(
            name__iexact=name
        ).exclude(
            id=company.id
        ).exists():

            raise ValidationError(
                {
                    "name": [
                        "Company name already exists."
                    ]
                }
            )

        # -----------------------------------------------------
        # DUPLICATE CODE
        # -----------------------------------------------------

        if code and Company.objects.filter(
            code__iexact=code
        ).exclude(
            id=company.id
        ).exists():

            raise ValidationError(
                {
                    "code": [
                        f"Company code '{code}' already exists."
                    ]
                }
            )

        # -----------------------------------------------------
        # BASIC FIELDS
        # -----------------------------------------------------

        company.name = name
        company.code = code

        for field in [
            "legal_name",
            "registration_number",
            "tax_id",
            "email",
            "phone",
            "website",
            "logo_url",
            "timezone",
            "currency",
            "date_format",
            "is_active",
        ]:

            if field in validated_data:
                setattr(
                    company,
                    field,
                    validated_data[field]
                )

        # -----------------------------------------------------
        # ADDRESS
        # -----------------------------------------------------

        if address_data is not None:

            for field in [
                "address_line_1",
                "address_line_2",
                "city",
                "state",
                "country",
                "postal_code",
            ]:

                if field in address_data:

                    setattr(
                        company,
                        field,
                        address_data[field]
                    )

        company.save()

        return company

    # =========================================================
    # DELETE
    # =========================================================

    @staticmethod
    @transaction.atomic
    def delete_company(company):

        company.is_active = False
        company.save(
            update_fields=[
                "is_active",
                "updated_at"
            ]
        )

        return company