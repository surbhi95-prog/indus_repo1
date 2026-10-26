import re

from apps.hrms.models.employee import Employee


def get_first_word(value):
    if not value:
        return "UNKNOWN"

    return value.strip().split()[0].upper()


def generate_employee_code(company, plant):

    company_prefix = get_first_word(company.name)
    plant_prefix = get_first_word(plant.name)

    prefix = f"{company_prefix}-{plant_prefix}-EMP"

    existing_codes = Employee.objects.filter(
        employee_code__startswith=prefix
    ).values_list(
        "employee_code",
        flat=True
    )

    max_number = 0

    pattern = re.compile(
        rf"^{re.escape(prefix)}(\d+)$"
    )

    for code in existing_codes:

        match = pattern.match(code)

        if match:

            number = int(
                match.group(1)
            )

            if number > max_number:
                max_number = number

    next_number = max_number + 1

    return f"{prefix}{next_number:03d}"