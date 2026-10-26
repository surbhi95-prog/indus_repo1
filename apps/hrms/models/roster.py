import uuid

from django.db import models

from apps.hrms.models.employee import Employee
from apps.hrms.models.shift import Shift
from apps.masters.models.company import Company
from apps.masters.models.department import Department
from apps.masters.models.plant import Plant


class Roster(models.Model):
    STATUS_CHOICES = (("ACTIVE", "Active"), ("INACTIVE", "Inactive"))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="hrms_rosters")
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="hrms_rosters")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name="hrms_rosters")
    name = models.CharField(max_length=150)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ACTIVE")
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by_name = models.CharField(max_length=255, blank=True)
    updated_by_name = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "rosters"
        constraints = [models.UniqueConstraint(fields=["company", "plant", "name", "start_date", "end_date"], condition=models.Q(is_deleted=False), name="unique_active_roster_period")]
        indexes = [models.Index(fields=["company", "plant", "start_date"]), models.Index(fields=["is_deleted"])]

    def __str__(self):
        return self.name


class RosterAssignment(models.Model):
    SOURCE_CHOICES = (
        ("manual", "Manual"),
        ("rotation", "Rotation"),
    )

    DAY_TYPE_CHOICES = (
        ("WORKING_DAY", "Working Day"),
        ("WEEK_OFF", "Week Off"),
        ("HOLIDAY", "Holiday"),
        ("LEAVE", "Leave"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    roster = models.ForeignKey(Roster, on_delete=models.CASCADE, related_name="assignments")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="roster_assignments")
    assignment_date = models.DateField()
    shift = models.ForeignKey(Shift, on_delete=models.PROTECT, null=True, blank=True, related_name="roster_assignments")
    day_type = models.CharField(max_length=20, choices=DAY_TYPE_CHOICES, default="WORKING_DAY", null=True, blank=True)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default="manual")
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by_name = models.CharField(max_length=255, blank=True)
    updated_by_name = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "roster_assignments"
        constraints = [models.UniqueConstraint(fields=["roster", "employee", "assignment_date"], condition=models.Q(is_deleted=False), name="unique_active_roster_employee_date")]
        indexes = [models.Index(fields=["roster", "assignment_date"]), models.Index(fields=["employee", "assignment_date"]), models.Index(fields=["is_deleted"])]

    def __str__(self):
        return f"{self.employee.employee_code} - {self.assignment_date}"
