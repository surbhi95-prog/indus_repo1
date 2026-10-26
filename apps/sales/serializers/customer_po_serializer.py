from apps.sales.models.customer_po import CustomerPO
from rest_framework import serializers
# from apps.sales.models
class CustomerPOCreateSerializer(serializers.ModelSerializer):

    def validate_name(self,val):
        val = val.strip()
        if not val:
            raise serializers.ValidationError("Customer name must be provided")

    class Meta:
        model = CustomerPO
        fields = "__all__"
        read_only_fields = ["id","po_number","updated_at","created_at"]


class CustomerPOResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerPO
        fields = "__all__"
        read_only_fields = ["id","po_number","updated_at","created_at"]
