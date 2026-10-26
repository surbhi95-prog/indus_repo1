# from rest_framework import serializers

# from apps.masters.models.company import Company
# from apps.masters.models.plant import Plant


# class PlantCreateSerializer(serializers.ModelSerializer):
#     """
#     Serializer for creating a Plant.
#     """

#     company = serializers.UUIDField(write_only=True)

#     class Meta:
#         model = Plant
#         fields = [
#             "company",
#             "name",
#             "location",
#         ]

#     def validate_company(self, value):

#         try:
#             company = Company.objects.get(id=value)

#         except Company.DoesNotExist:
#             raise serializers.ValidationError(
#                 "Company does not exist."
#             )

#         return company

#     def validate_name(self, value):

#         value = value.strip()

#         if not value:
#             raise serializers.ValidationError(
#                 "Plant name is required."
#             )

#         return value

#     def validate(self, attrs):

#         company = attrs["company"]
#         name = attrs["name"]

#         if Plant.objects.filter(
#             company=company,
#             name__iexact=name
#         ).exists():

#             raise serializers.ValidationError(
#                 {
#                     "name": "Plant already exists for this company."
#                 }
#             )

#         return attrs


# class PlantListSerializer(serializers.ModelSerializer):

#     company_name = serializers.CharField(
#         source="company.name",
#         read_only=True
#     )

#     class Meta:
#         model = Plant
#         fields = [
#             "id",
#             "company_name",
#             "name",
#             "location",
#             "is_active",
#             "created_at",
#             "updated_at",
#         ]


# class PlantDetailSerializer(serializers.ModelSerializer):

#     company_name = serializers.CharField(
#         source="company.name",
#         read_only=True
#     )

#     class Meta:
#         model = Plant
#         fields = [
#             "id",
#             "company",
#             "company_name",
#             "name",
#             "location",
#             "is_active",
#             "created_at",
#             "updated_at",
#         ]


# class PlantUpdateSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Plant
#         fields = [
#             "name",
#             "location",
#             "is_active",
#         ]

#     def validate_name(self, value):

#         value = value.strip()

#         if not value:
#             raise serializers.ValidationError(
#                 "Plant name is required."
#             )

#         if Plant.objects.filter(
#             company=self.instance.company,
#             name__iexact=value
#         ).exclude(
#             id=self.instance.id
#         ).exists():

#             raise serializers.ValidationError(
#                 "Plant already exists."
#             )

#         return value



from rest_framework import serializers

from apps.masters.models.company import Company
from apps.masters.models.plant import Plant


# =============================================================
# ADDRESS
# =============================================================

class PlantAddressSerializer(serializers.Serializer):

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


# =============================================================
# CONTACT
# =============================================================

class PlantContactSerializer(serializers.Serializer):

    email = serializers.EmailField(
        required=False,
        allow_blank=True,
        allow_null=True
    )

    phone = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True
    )


# =============================================================
# CREATE
# =============================================================

class PlantCreateSerializer(serializers.ModelSerializer):

    company = serializers.UUIDField(
        write_only=True
    )

    address = PlantAddressSerializer(
        required=False
    )

    contact = PlantContactSerializer(
        required=False
    )

    class Meta:
        model = Plant

        fields = [
            "company",
            "name",
            "code",
            "plant_type",
            "address",
            "contact",
            "timezone",
        ]

    # ---------------------------------------------------------
    # COMPANY
    # ---------------------------------------------------------

    def validate_company(self, value):

        try:
            return Company.objects.get(
                id=value,
                is_active=True
            )

        except Company.DoesNotExist:

            raise serializers.ValidationError(
                "Company does not exist or is inactive."
            )

    # ---------------------------------------------------------
    # NAME
    # ---------------------------------------------------------

    def validate_name(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Plant name is required."
            )

        return value

    # ---------------------------------------------------------
    # CODE
    # ---------------------------------------------------------

    def validate_code(self, value):

        value = value.strip().upper()

        if not value:
            raise serializers.ValidationError(
                "Plant code is required."
            )

        return value

    # ---------------------------------------------------------
    # DUPLICATE VALIDATION
    # ---------------------------------------------------------

    def validate(self, attrs):

        company = attrs["company"]
        name = attrs["name"]
        code = attrs["code"]

        if Plant.objects.filter(
            company=company,
            name__iexact=name
        ).exists():

            raise serializers.ValidationError(
                {
                    "name": [
                        "Plant name already exists for this company."
                    ]
                }
            )

        if Plant.objects.filter(
            company=company,
            code__iexact=code
        ).exists():

            raise serializers.ValidationError(
                {
                    "code": [
                        "Plant code already exists for this company."
                    ]
                }
            )

        return attrs
class PlantListSerializer(serializers.ModelSerializer):

    address = serializers.SerializerMethodField()

    contact = serializers.SerializerMethodField()

    company_name = serializers.CharField(
        source="company.name",
        read_only=True
    )

    class Meta:
        model = Plant

        fields = [
            "id",
            "company",
            "company_name",
            "name",
            "code",
            "plant_type",
            "address",
            "contact",
            "timezone",
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

    def get_contact(self, obj):

        return {
            "email": obj.email,
            "phone": obj.phone,
        }
class PlantDetailSerializer(PlantListSerializer):
    pass


class PlantDetailsSerializer(PlantListSerializer):
    created_by_name = serializers.SerializerMethodField()
    updated_by_name = serializers.SerializerMethodField()
    employee_count = serializers.IntegerField(read_only=True)
    department_count = serializers.IntegerField(read_only=True)

    class Meta(PlantListSerializer.Meta):
        fields = PlantListSerializer.Meta.fields + [
            "created_by_name",
            "updated_by_name",
            "employee_count",
            "department_count",
        ]

    @staticmethod
    def _user_name(obj, relationship):
        user = getattr(obj, relationship, None)
        if user is None:
            return None
        full_name = f"{getattr(user, 'first_name', '') or ''} {getattr(user, 'last_name', '') or ''}".strip()
        return full_name or getattr(user, "username", None) or getattr(user, "email", None)

    def get_created_by_name(self, obj):
        return self._user_name(obj, "created_by")

    def get_updated_by_name(self, obj):
        return self._user_name(obj, "updated_by")

class PlantUpdateSerializer(serializers.ModelSerializer):

    address = PlantAddressSerializer(
        required=False
    )

    contact = PlantContactSerializer(
        required=False
    )

    class Meta:
        model = Plant

        fields = [
            "name",
            "code",
            "plant_type",
            "address",
            "contact",
            "timezone",
            "is_active",
        ]

    # ---------------------------------------------------------
    # NAME
    # ---------------------------------------------------------

    def validate_name(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Plant name is required."
            )

        plant = self.instance

        if Plant.objects.filter(
            company=plant.company,
            name__iexact=value
        ).exclude(
            id=plant.id
        ).exists():

            raise serializers.ValidationError(
                "Plant name already exists for this company."
            )

        return value

    # ---------------------------------------------------------
    # CODE
    # ---------------------------------------------------------

    def validate_code(self, value):

        value = value.strip().upper()

        plant = self.instance

        if Plant.objects.filter(
            company=plant.company,
            code__iexact=value
        ).exclude(
            id=plant.id
        ).exists():

            raise serializers.ValidationError(
                "Plant code already exists for this company."
            )

        return value
