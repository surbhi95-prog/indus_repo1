from django.urls import path

from apps.masters.views.company_view import (
    CompanyListCreateView,
    CompanyDetailView,
)
from apps.masters.views.plant_view import (
    PlantDetailView,
    PlantDetailsView,
    PlantView,
)
from apps.masters.views.department_view import (
    DepartmentView,
    DepartmentDetailView,
)
urlpatterns = [

    path(
        "/companies",
        CompanyListCreateView.as_view(),
        name="company-list-create",
    ),

    path(
        "/companies/<uuid:company_id>",
        CompanyDetailView.as_view(),
        name="company-detail",
    ),
        path(
            "/plants/",
            PlantView.as_view(),
            name="plant-list-create",
        ),

        path(
            "/plants/<uuid:plant_id>",
            PlantDetailView.as_view(),
            name="plant-detail",
        ),
        path(
            "/plants/<uuid:plant_id>/details/",
            PlantDetailsView.as_view(),
            name="plant-details",
        ),
    path(
        "/departments/",
        DepartmentView.as_view(),
        name="department-list-create",
    ),

    path(
        "/departments/<uuid:department_id>/",
        DepartmentDetailView.as_view(),
        name="department-detail",
    ),

]
