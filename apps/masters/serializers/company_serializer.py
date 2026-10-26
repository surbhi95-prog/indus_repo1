# from rest_framework import serializers

# from apps.masters.models.company import Company


# class CompanyCreateSerializer(serializers.ModelSerializer):
#     """
#     Serializer for creating a company.
#     """

#     class Meta:
#         model = Company
#         fields = [
#             "name",
#             "code",
#         ]

#     def validate_name(self, value):
#         value = value.strip()

#         if not value:
#             raise serializers.ValidationError(
#                 "Company name is required."
#             )

#         return value

#     def validate_code(self, value):
#         if value:
#             value = value.strip().upper()

#         return value


# class CompanyListSerializer(serializers.ModelSerializer):
#     """
#     Serializer for listing companies.
#     """

#     class Meta:
#         model = Company
#         fields = [
#             "id",
#             "name",
#             "code",
#             "is_active",
#             "created_at",
#             "updated_at",
#         ]


# class CompanyDetailSerializer(serializers.ModelSerializer):
#     """
#     Serializer for company details.
#     """

#     class Meta:
#         model = Company
#         fields = [
#             "id",
#             "name",
#             "code",
#             "is_active",
#             "created_at",
#             "updated_at",
#         ]


# class CompanyUpdateSerializer(serializers.ModelSerializer):
#     """
#     Serializer for updating a company.
#     """

#     class Meta:
#         model = Company
#         fields = [
#             "name",
#             "code",
#             "is_active",
#         ]

#     def validate_name(self, value):
#         value = value.strip()

#         if not value:
#             raise serializers.ValidationError(
#                 "Company name is required."
#             )

#         return value

#     def validate_code(self, value):

#       if value:
#         value = value.strip().upper()

#         if Company.objects.filter(
#             code__iexact=value
#         ).exists():
#             raise serializers.ValidationError(
#                 "Company code already exists."
#             )

#         return value




from rest_framework import serializers

from apps.masters.models.company import Company


class CompanyAddressSerializer(serializers.Serializer):

    address_line_1 = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True
    )

    address_line_2 = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True
    )

    city = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True
    )

    state = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True
    )

    country = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True
    )

    postal_code = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True
    )


class CompanyCreateSerializer(serializers.ModelSerializer):

    address = CompanyAddressSerializer(
        required=False
    )

    class Meta:
        model = Company

        fields = [
            "name",
            "code",
            "legal_name",
            "registration_number",
            "tax_id",
            "email",
            "phone",
            "website",
            "address",
            "logo_url",
            "timezone",
            "currency",
            "date_format",
        ]

    def validate_name(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Company name is required."
            )

        return value

    def validate_code(self, value):

        if value:
            value = value.strip().upper()

        return value

class CompanyListSerializer(serializers.ModelSerializer):

    address = serializers.SerializerMethodField()

    class Meta:
        model = Company

        fields = [
            "id",
            "name",
            "code",
            "legal_name",
            "registration_number",
            "tax_id",
            "email",
            "phone",
            "website",
            "address",
            "logo_url",
            "timezone",
            "currency",
            "date_format",
            "is_active",
            "created_at",
            "updated_at",
        ]

    def get_address(self, obj):

        return {
            "address_line_1": obj.address_line_1,
            "address_line_2": obj.address_line_2,
            "city": obj.city,
            "state": obj.state,
            "country": obj.country,
            "postal_code": obj.postal_code,
        }
class CompanyUpdateSerializer(serializers.ModelSerializer):

    address = CompanyAddressSerializer(
        required=False
    )

    class Meta:
        model = Company

        fields = [
            "name",
            "code",
            "legal_name",
            "registration_number",
            "tax_id",
            "email",
            "phone",
            "website",
            "address",
            "logo_url",
            "timezone",
            "currency",
            "date_format",
            "is_active",
        ]

    def validate_name(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Company name is required."
            )

        return value

    def validate_code(self, value):

        if value:
            value = value.strip().upper()

        company = self.instance

        if value and Company.objects.filter(
            code__iexact=value
        ).exclude(
            id=company.id
        ).exists():

            raise serializers.ValidationError(
                "Company code already exists."
            )

        return value
class CompanyDetailSerializer(CompanyListSerializer):
    pass