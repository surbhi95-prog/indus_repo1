from apps.sales.models.customer import Customer
from rest_framework.exceptions import NotFound
from django.db.models import Max, IntegerField
from django.db.models.functions import Cast, Substr
class CustomerService:

    @staticmethod
    def create_user(validated_data):
        # cust_code = generate_cust_code()

        def generate_cust_code():
        
                result = (
                    Customerr.objects
                    .filter(cust_code__regex=r"^CP[0-9]+$")
                    .annotate( # adds a value to each record being generated
                        suffix=Cast(  # Cast converts 007 to 7
                            Substr("cust_code", 3), # extracts string from where the numbers start
                            IntegerField()
                        )
                    )
                    .aggregate(max_suffix=Max("suffix"))
                )
        
                next_number = (result["max_suffix"] or 0) + 1
        
                return f"CP{next_number:03d}" # next number should atleast 3 digits
        cust_code = generate_cust_code()
        # data = validated_data.copy()
        # id = data.pop("id")
        # cust= Customerr.objects.exists(id=id)
        # if not cust:
        cust = Customerr.objects.create(cust_code=cust_code,**validated_data)
        return cust

    @staticmethod
    def list_all_cust():
        return Customerr.objects.all().order_by("-created_at")

    @staticmethod
    def get_by_id(id):
        return Customerr.objects.get(id=id)


    @staticmethod
    def update_cust(validated_data,id):
        try:
            cust = Customerr.objects.get(id=id)
        except Customerr.DoesNotExist:
            raise NotFound("Customer with this ID does not exist")
        for fields,val in validated_data.items():
            setattr(cust,fields,val)
        cust.save()
        return cust
    # def update_cust(id,validated_data):
    #     try:
    #         cust = Customerr.objects.get(id=id)
    #     except Customerr.DoesNotExist:
    #         raise NotFound("Customer Not Found")

    #     for field,value in validated_data.items():
    #         setattr(cust,field,value)

    #     cust.save()

    #     return cust


    @staticmethod
    def patch_cust(validated_data,id):
        try:
            cust = Customerr.objects.get(id=id)
        except Customerr.DoesNotExist:
            raise NotFound("Id not found")
        for fields, vals in validated_data.items():
            setattr(cust,fields,vals)

        cust.save()
        return cust

    # def patch_cust(id,validated_data):

    #     try:
    #         cust = Customerr.objects.get(id=id)

    #     except Customerr.DoesNotExist:
    #         raise NotFound("Cust with this code does not exist")

    #     for field,val in validated_data.items():
    #         setattr(cust,field,val)

    #     cust.save()
    #     return cust

    @staticmethod
    def delete_by_id(id):
         try:
            emp = Customerr.objects.get(id=id)
         except Customerr.DoesNotExist:
             raise NotFound("This cust code does not exist")

         emp.delete()

    @staticmethod
    def delete_all():
        cust = Customerr.objects.all()

        cust.delete()


# from appcustomer.customerr import Customerr


    # def generate_cust_code():

    #     result = (
    #         Customerr.objects
    #         .filter(cust_code__regex=r"^CP[0-9]+$")
    #         .annotate( # adds a value to each record being generated
    #             suffix=Cast(  # Cast converts 007 to 7
    #                 Substr("cust_code", 3), # extracts string from where the numbers start
    #                 IntegerField()
    #             )
    #         )
    #         .aggregate(max_suffix=Max("suffix"))
    #     )

    #     next_number = (result["max_suffix"] or 0) + 1

    #     return f"CP{next_number:03d}" # next number should atleast 3 digits