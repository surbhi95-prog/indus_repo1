from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.sales.services.customer_service import (CustomerService)
from apps.sales.serializers.customer_seri import (CustomerReqSerializer,CustomerResponseSerializer,CustomerResSerializer)

# from sales.models.customer import Customerr
class CustomerView(APIView):

    def post(self,request):
        serializer = CustomerReqSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        cust = CustomerService.create_user(serializer.validated_data)

        response_serializing = CustomerResSerializer(
            cust
        )
        return Response(
            response_serializing.data,
            status= status.HTTP_201_CREATED
        )

    def get(self,request):

        # ---------- IF NO FILTERS, DISPLAY ALL -------------
        if not request.query_params:

            customers = CustomerService.list_all_cust()

            reponse_ser = CustomerResponseSerializer(customers,many=True)
            return Response(
                reponse_ser.data,
                status=status.HTTP_200_OK
            )

        # apply the filter
        custs = Customerr.objects.all()

        params = request.query_params

        allowed_filters = [
            "cust_type",
            "state",
            # "cust_name",
            # "email",
            "city",
            "payment_terms",
            "status",
            # "created_at",
        ]

        filter_mapping ={
            "cust_type":"cust_type__iexact",
            "state":"state__iexact",
            "city":"city__iexact",
            "payment_terms":"payment_terms__iexact",
            "status":"status__iexact",
            # "created_at":""
        }

        
        # iterate thru allowed_filters
        for param in filter_mapping.items():
            # check if the value is actually asked in the filter
            val = params.get(param)

            if val is not None and val!="":
                # Passing each pair to the filter
                custs = custs.filter(
                    **{param:val}
                )

        response_ser = CustomerResponseSerializer(
        custs,
        many=True
        )

        return Response(
            response_ser.data,
            status=status.HTTP_200_OK
        )

    def delete(self,request):

        cust = CustomerService.delete_all()
        return Response(
            {
                "msg":"Deleted all!"
            },
            status=status.HTTP_200_OK
        )
    # def get(self,request,cust_code):

    #     # serialzer = CustomerReqSerializer(cust_code)

    #     # serialzer.is_valid(raise_exception=True)

    #     customer = CustomerService.get_by_id(cust_code)

    #     resp = CustomerResponseSerializer(customer)

    #     return Response(
    #         resp.data,
    #         status=status.HTTP_200_OK
    #     )


class CustomerByIdView(APIView):
   def get(self,request,id):

        # serialzer = CustomerReqSerializer(cust_code)

        # serialzer.is_valid(raise_exception=True)

        customer = CustomerService.get_by_id(id)

        resp = CustomerResponseSerializer(customer)

        return Response(
            resp.data,
            status=status.HTTP_200_OK
        )

#    def put(self,request,id):
#        seri = CustomerReqSerializer(data=request.data,  context={"id":id})

#        seri.is_valid(
#            raise_exception=True,
#         )

#        cust = CustomerService.update_cust(
#            id,
#            seri.validated_data
#        )

#        resp = CustomerResponseSerializer(
#            cust
#        )

#        return Response(
#            resp.data,
#            status=status.HTTP_200_OK
#        )
   
   
   
   
   
   def put(self,request,id):
       seri = CustomerReqSerializer(
           data=request.data,
           context={"id":id}
       )

       seri.is_valid(raise_exception=True)

       cust = CustomerService.update_cust(seri.validated_data,id)

       resp = CustomerResponseSerializer(cust)
       return Response(
           resp.data,
           status=status.HTTP_200_OK
       )

   def patch(self,request,id):
       if not request.data:
           return Response(
               {"message":"Pass atleast one k-v pair"}
           )
           
       seri = CustomerReqSerializer(
           data=request.data,
           partial=True,
           context={"id":id}
       )

       seri.is_valid(raise_exception=True)

       cust = CustomerService.patch_cust(seri.validated_data,id)

       resp = CustomerResponseSerializer(
           cust
       )

       return Response(
           resp.data,
           status=status.HTTP_200_OK
       )
   
#    def patch(self,request,id):
#        seri = CustomerReqSerializer(
#            data=request.data,
#            partial=True,
#            context={"id":id}
#        )

#        seri.is_valid(raise_exception=True)

#        cust = CustomerService.patch_cust(id,seri.validated_data)

#        resp = CustomerResponseSerializer(
#            cust
#        )
#        return Response(
#            resp.data,
#            status=status.HTTP_200_OK
#        )

   def delete(self,request,id):

    #    seri = CustomerReqSerializer(
    #        data=request.validatedata
    #    )

    #    seri.is_valid(raise_exception=True)

       cust = CustomerService.delete_by_id(id)

       resp = CustomerResponseSerializer(
           cust
       )

       return Response(
           resp.data,
           status=status.HTTP_200_OK
       )


class EmployeeListFilterView(APIView):
    def get(self,request):

        # if request.query_params:
            

        # fetch the value of the field passed
        status_val = request.query_params.get("status")

        # if value is found, fetch for it in the Table
        if status_val:
            result = Customerr.objects.all().filter(status=status_val)

        resp = CustomerResponseSerializer(result,many=True)
        return Response(
            resp.data,
            status=status.HTTP_200_OK
        )

        