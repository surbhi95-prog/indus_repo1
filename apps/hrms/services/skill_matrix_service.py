from apps.hrms.models.employee_skill import EmployeeSkill
from apps.hrms.models.department_skill import DepartmentSkill


class SkillMatrixService:

    @staticmethod
    def get_employee_matrix(employee):

        department_skills = (
            DepartmentSkill.objects
            .filter(
                company_id=employee.company_id,
                plant_id=employee.plant_id,
                department_id=employee.department_id,
                is_active=True,
            )
            .select_related("skill")
        )

        employee_skills = {
            item.skill_id: item
            for item in EmployeeSkill.objects.filter(
                employee=employee
            )
        }

        result = []

        for department_skill in department_skills:

            employee_skill = employee_skills.get(
                department_skill.skill_id
            )

            current_level = (
                employee_skill.current_level
                if employee_skill
                else 0
            )

            required_level = (
                department_skill.required_level
            )

            gap = max(
                required_level - current_level,
                0
            )

            if current_level >= required_level:
                status = "qualified"

            elif current_level == 0:
                status = "not_assessed"

            else:
                status = "skill_gap"

            result.append({

                "skill_id":
                    department_skill.skill_id,

                "skill":
                    department_skill.skill.name,

                "skill_code":
                    department_skill.skill.code,

                "required_level":
                    required_level,

                "current_level":
                    current_level,

                "gap":
                    gap,

                "status":
                    status,

                "mandatory":
                    department_skill.is_mandatory,

                "certified":
                    (
                        employee_skill.is_certified
                        if employee_skill
                        else False
                    ),
            })

        return result   