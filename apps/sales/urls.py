from django.contrib import admin
from django.urls import path,include
from apps.sales.views.customer_view import (CustomerView, CustomerByIdView)
# from views import
urlpatterns = [
    # path('api/cust',apps.app1.urls, name = "customer"),


    path(
        "create/",
        CustomerView.as_view(),
        name="create-cust",
    ),

    # DONE
    path(
        "list/",
        CustomerView.as_view(),
        name="list-cust",
    ),

    # DONE
    path(
            "get_by_id/<int:id>",
            CustomerByIdView.as_view(),
            name="cust_detail",
        ),

    path(
        "put/<int:id>",
        CustomerByIdView.as_view(),
        name="update-cust",
    ),

    # DONE
    path(
                "patch/<int:id>",
                CustomerByIdView.as_view(),
                name="patch-cust",
            ),

    # DONE
    path(
        "delete_by_id/<int:id>",
        CustomerByIdView.as_view(),
        name='del-by-code'
    ),

    path("delete_all/",
         CustomerView.as_view(),
         name='del-all'
    ),
]
    # path("count",)
    
    

    # FILTERSS ------------------------------------
    # path(
    #         "get/?<status:str>",
    #         CustomerView.as_view(),
    #         name="status-filter",),


# urlpatterns = [
#     # path("customers/", CustomerView.as_view(), name="customers"),
#     path("customers/", CustomerView.as_view(), name="customers"),

#     path(
#         "customers/<int:id>/",
#         CustomerByIdView.as_view(),
#         name="customer-detail",
#     ),
# ]