# from rest_framework import serializers

# from apps.inventory.models.uom import UOM


# class UOMSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = UOM
#         fields = [
#             "id",
#             "company",
#             "plant",
#             "name",
#             "code",
#             "is_active",
#             "created_at",
#         ]

#         read_only_fields = [
#             "id",
#             "created_at",
#         ]

#     def validate(self, attrs):

#         plant = attrs.get("plant")
#         company = attrs.get("company")

#         if plant and company:
#             if plant.company_id != company.id:
#                 raise serializers.ValidationError(
#                     "Plant does not belong to the selected company."
#                 )

#         return attrs


from rest_framework import serializers

from apps.inventory.models.uom import UOM


class UOMSerializer(serializers.ModelSerializer):

    class Meta:
        model = UOM

        fields = [
            "id",
            "company",
            "plant",
            "name",
            "code",
            "is_active",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]

    def validate(self, attrs):

        company = attrs.get(
            "company",
            getattr(self.instance, "company", None)
        )

        plant = attrs.get(
            "plant",
            getattr(self.instance, "plant", None)
        )

        if plant and company:

            if plant.company_id != company.id:
                raise serializers.ValidationError({
                    "plant": "Plant does not belong to the selected company."
                })

        return attrs