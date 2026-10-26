from apps.accounts.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.hrms.models.employee import Employee
from apps.hrms.models.department_skill import DepartmentSkill
from apps.hrms.models.employee_skill import EmployeeSkill


class EmployeeSkillMatrixView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request, employee_id):

        try:

            employee = (
                Employee.objects
                .select_related(
                    "company",
                    "plant",
                    "department"
                )
                .get(id=employee_id)
            )

        except Employee.DoesNotExist:

            return Response({
                "success": False,
                "message": "Employee not found."
            }, status=404)

        required_skills = (
            DepartmentSkill.objects
            .filter(
                department=employee.department
            )
            .select_related("skill")
        )

        employee_skills = {
            item.skill_id: item
            for item in EmployeeSkill.objects.filter(
                employee=employee
            )
        }

        matrix = []

        for required in required_skills:

            employee_skill = employee_skills.get(
                required.skill_id
            )

            current_level = (
                employee_skill.level
                if employee_skill
                else 0
            )

            matrix.append({
                "skill_id": str(
                    required.skill.id
                ),
                "skill": required.skill.name,
                "code": required.skill.code,
                "mandatory":
                    required.is_mandatory,
                "minimum_level":
                    required.minimum_level,
                "target_level":
                    required.target_level,
                "current_level":
                    current_level,
                "gap":
                    max(
                        required.target_level
                        - current_level,
                        0
                    ),
                "status":
                    "qualified"
                    if current_level >= required.target_level
                    else "gap"
            })

        return Response({
            "success": True,
            "employee": {
                "id": str(employee.id),
                "employee_code":
                    employee.employee_code,
                "name":
                    f"{employee.first_name} "
                    f"{employee.last_name}".strip(),
                "department":
                    employee.department.name
                    if employee.department
                    else None
            },
            "skills": matrix
        })


class DepartmentSkillMatrixView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request, department_id):

        employees = (
            Employee.objects
            .filter(
                department_id=department_id,
                status="active"
            )
            .order_by("employee_code")
        )

        required_skills = (
            DepartmentSkill.objects
            .filter(
                department_id=department_id
            )
            .select_related("skill")
        )

        employee_ids = employees.values_list(
            "id",
            flat=True
        )

        employee_skills = (
            EmployeeSkill.objects
            .filter(
                employee_id__in=employee_ids
            )
            .select_related(
                "employee",
                "skill"
            )
        )

        skill_map = {}

        for item in employee_skills:

            skill_map[
                (
                    item.employee_id,
                    item.skill_id
                )
            ] = item.level

        matrix = []

        for employee in employees:

            employee_data = {
                "employee_id":
                    str(employee.id),

                "employee_code":
                    employee.employee_code,

                "employee_name":
                    f"{employee.first_name} "
                    f"{employee.last_name}".strip(),

                "skills": []
            }

            for required in required_skills:

                current_level = skill_map.get(
                    (
                        employee.id,
                        required.skill_id
                    ),
                    0
                )

                employee_data["skills"].append({
                    "skill_id":
                        str(required.skill.id),

                    "skill":
                        required.skill.name,

                    "current_level":
                        current_level,

                    "minimum_level":
                        required.minimum_level,

                    "target_level":
                        required.target_level,

                    "gap":
                        max(
                            required.target_level
                            - current_level,
                            0
                        ),

                    "status":
                        "qualified"
                        if current_level >= required.target_level
                        else "gap"
                })

            matrix.append(employee_data)

        return Response({
            "success": True,
            "department_id":
                str(department_id),
            "employees": matrix
        })