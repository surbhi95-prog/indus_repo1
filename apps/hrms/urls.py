from django.urls import path

from apps.hrms.views.user_view import (
    UserCreateView,
    UserDetailView,
    UserListView,
)
from apps.hrms.views.employee_document_view import EmployeeDocumentView

from apps.hrms.views.skill_view import (
    SkillListCreateView,
    SkillDetailView
)

from apps.hrms.views.department_skill_view import (
    DepartmentSkillListCreateView
)

from apps.hrms.views.employee_skill_view import (
    EmployeeSkillListCreateView,
    EmployeeSkillDetailView
)

from apps.hrms.views.skill_matrix_view import (
    EmployeeSkillMatrixView,
    DepartmentSkillMatrixView
)
from apps.hrms.views.attendance import (
    AttendanceViewSet,
    AttendanceLogViewSet,
)
from apps.hrms.views.shift_view import (
    ShiftListCreateView,
)
from apps.hrms.views.biometric import (
    BiometricDeviceViewSet,
    BiometricEmployeeViewSet,
    BiometricPunchViewSet,
)

from apps.hrms.views.attendance_import import (
    AttendanceImportViewSet,
)
from apps.hrms.views.roster_view import (
    RosterAssignmentDetailView,
    RosterAssignmentListView,
    RosterAssignView,
    RosterDetailView,
    RosterListCreateView,
    RosterRotateView,
)


urlpatterns = [

    # HRMS Rosters (8 API methods across these routes)
    path("/rosters/", RosterListCreateView.as_view(), name="roster-list-create"),
    path("/rosters/<uuid:roster_id>/", RosterDetailView.as_view(), name="roster-detail"),
    path("/rosters/<uuid:roster_id>/assign/", RosterAssignView.as_view(), name="roster-assign"),
    path("/rosters/<uuid:roster_id>/rotate/", RosterRotateView.as_view(), name="roster-rotate"),
    path("/roster-assignments/", RosterAssignmentListView.as_view(), name="roster-assignment-list"),
    path("/roster-assignments/<uuid:assignment_id>/", RosterAssignmentDetailView.as_view(), name="roster-assignment-detail"),

    # User
    path(
        "/users/create/",
        UserCreateView.as_view(),
        name="user-create",
    ),
    path(
        "/documents/<uuid:document_id>/view/",
        EmployeeDocumentView.as_view(),
        name="employee-document-view",
    ),
    path(
        "/skills/",
        SkillListCreateView.as_view(),
        name="skill-list-create"
    ),

    path(
        "/skills/<uuid:skill_id>/",
        SkillDetailView.as_view(),
        name="skill-detail"
    ),

    # =====================================================
    # DEPARTMENT SKILLS
    # =====================================================

    path(
        "/department-skills/",
        DepartmentSkillListCreateView.as_view(),
        name="department-skill-list-create"
    ),

    # =====================================================
    # EMPLOYEE SKILLS
    # =====================================================

    path(
        "/employee-skills/",
        EmployeeSkillListCreateView.as_view(),
        name="employee-skill-list-create"
    ),

    path(
        "/employee-skills/<uuid:skill_id>/",
        EmployeeSkillDetailView.as_view(),
        name="employee-skill-detail"
    ),

    # =====================================================
    # SKILL MATRIX
    # =====================================================

    path(
        "employees/<uuid:employee_id>/skill-matrix/",
        EmployeeSkillMatrixView.as_view(),
        name="employee-skill-matrix"
    ),

    path(
        "departments/<uuid:department_id>/skill-matrix/",
        DepartmentSkillMatrixView.as_view(),
        name="department-skill-matrix"
    ),
    path(
        "/attendance/",
        AttendanceViewSet.as_view({
            "get": "list",
            "post": "create",
        }),
        name="attendance-list",
    ),
        # ------------------------------------------
    # Shift Management
    # ------------------------------------------

    path(
        "/shifts/",
        ShiftListCreateView.as_view(),
        name="shift-list-create",
    ),
    path(
        "/attendance/today-summary/",
        AttendanceViewSet.as_view({
            "get": "today_summary",
        }),
        name="attendance-today-summary",
    ),
    path(
        "/attendance/<uuid:pk>/",
        AttendanceViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="attendance-detail",
    ),

    # ------------------------------------------
    # Attendance Logs
    # ------------------------------------------

    path(
        "/attendance-logs/",
        AttendanceLogViewSet.as_view({
            "get": "list",
            "post": "create",
        }),
        name="attendance-log-list",
    ),

    path(
        "/attendance-logs/<uuid:pk>/",
        AttendanceLogViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="attendance-log-detail",
    ),

    # ------------------------------------------
    # Biometric Devices
    # ------------------------------------------

    path(
        "/biometric/devices/",
        BiometricDeviceViewSet.as_view({
            "get": "list",
            "post": "create",
        }),
        name="biometric-device-list",
    ),

    path(
        "/biometric/devices/<uuid:pk>/",
        BiometricDeviceViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="biometric-device-detail",
    ),

    # ------------------------------------------
    # Biometric Employees
    # ------------------------------------------

    path(
        "/biometric/employees/",
        BiometricEmployeeViewSet.as_view({
            "get": "list",
            "post": "create",
        }),
        name="biometric-employee-list",
    ),

    path(
        "/biometric/employees/<uuid:pk>/",
        BiometricEmployeeViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="biometric-employee-detail",
    ),

    # ------------------------------------------
    # Biometric Punches
    # ------------------------------------------

    path(
        "/biometric/punches/",
        BiometricPunchViewSet.as_view({
            "get": "list",
            "post": "create",
        }),
        name="biometric-punch-list",
    ),

    path(
        "/biometric/punches/<uuid:pk>/",
        BiometricPunchViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="biometric-punch-detail",
    ),

    # ------------------------------------------
    # Attendance Import
    # ------------------------------------------

    path(
        "/attendance-imports/",
        AttendanceImportViewSet.as_view({
            "get": "list",
            "post": "create",
        }),
        name="attendance-import-list",
    ),

    path(
        "/attendance-imports/<uuid:pk>/",
        AttendanceImportViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="attendance-import-detail",
    ),


    path(
        "/users/list/",
        UserListView.as_view(),
        name="user-list",
    ),

    # Fetch user by ID
    path(
        "/users/<uuid:user_id>/",
        UserDetailView.as_view(),
        name="user-detail",
    ),


]
