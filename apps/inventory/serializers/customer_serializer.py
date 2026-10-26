from rest_framework import serializers
from apps.sales.models.customer import Customer
# from 
import re
class CustomerReqSerializer(serializers.ModelSerializer):

    def validate_phone(self, value):
        value = value.strip()

        # + is optional
        # pattern = r"^(?:\+91[\s-]?|91[\s-]?|0)?[6-9]\d{9}$"

        # +91 is req
        # number should start with numbers b/wn 6-9 and then followed by 9 digits 
        pattern = r"^\+91[6-9]\d{9}$"

        # if len(value) :
        #      pass
        if not re.fullmatch(pattern, value):
            raise serializers.ValidationError(
                "Enter a valid Indian mobile number."
                "Must start with +91. eg: (+917xxxxxxxx)."
            )

        return value



    def validate_gst_number(self, value):
        value = value.strip().upper()

        # 27
        pattern = (
            r"^[0-9]{2}"
            r"[A-Z]{5}[0-9]{4}[A-Z]"
            r"[1-9A-Z]"
            r"Z"
            r"[0-9A-Z]$"
        )

        if len(value) != 15 or not re.fullmatch(pattern, value):
            raise serializers.ValidationError(
                "Enter a valid 15-character Indian GSTIN."
            )
        return value

    def validate_email(self,value):
            value = value.strip().lower()


            # filter emps by mail
            emps = Customerr.objects.filter(email=value)

            # exclude the emp's record from the resultset 
            # so user who is making req will be excluded and if still resultset exists... the mail is duplicate
            if self.instance:
                emps = emps.exclude(pk=self.instance.pk)

            if emps.exists():
                raise serializers.ValidationError(
                "An employee with this email already exists."
            )

            return value

    # Ithe contact_person cha name peksha naav ani number donhi pahije
    # def validate_contact_person(self,value):
    #     if value is None:
    #         raise serializers.ValidationError("Contact Person's name must be provided.")

        # if not value.strip():
        #     raise serializers.ValidationError("Contact Person's name must be provided.")
        
    class Meta:
        model = Customer
        fields = "__all__"
        read_only_fields = ["cust_code"]

class CustomerResSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"

class CustomerResponseSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        cust_code = serializers.CharField(max_length=20)
        cust_name = serializers.CharField(max_length=100)
        cust_type = serializers.CharField()
    
        contact_person = serializers.CharField(max_length=100)
        email = serializers.EmailField()
        status = serializers.CharField()
        phone = serializers.CharField(max_length=10)
        address_line = serializers.CharField()
        city = serializers.CharField(max_length=100)
        state = serializers.CharField(max_length=100)
        gst_number = serializers.CharField(max_length=15)
        payment_terms = serializers.CharField()
        status = serializers.CharField()
        # class Meta:
        #      model = Customer
        #      fields = "__all__"

# class CustomerPutSerializer(serializers.Serializer):

