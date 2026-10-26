# from datetime import datetime

# from django.db import transaction

# from openpyxl import load_workbook

# from apps.hrms.models.employee import Employee
# from apps.hrms.models.attendance_import_row import (
#     AttendanceImportRow
# )

# from apps.hrms.services.attendance_service import (
#     AttendanceService
# )


# class ExcelAttendanceService:

#     @staticmethod
#     @transaction.atomic
#     def process_import(attendance_import):

#         attendance_import.status = "processing"
#         attendance_import.save(
#             update_fields=["status"]
#         )

#         try:

#             workbook = load_workbook(
#                 attendance_import.file.path,
#                 data_only=True
#             )

#             worksheet = workbook.active

#             rows = list(
#                 worksheet.iter_rows(
#                     values_only=True
#                 )
#             )

#             if not rows:

#                 attendance_import.status = "failed"
#                 attendance_import.error_message = (
#                     "Excel file is empty."
#                 )
#                 attendance_import.save()

#                 return attendance_import

#             headers = [
#                 str(value).strip().lower()
#                 if value is not None
#                 else ""
#                 for value in rows[0]
#             ]

#             required_headers = [
#                 "employee_code",
#                 "date",
#                 "in_time",
#                 "out_time",
#             ]

#             missing_headers = [
#                 header
#                 for header in required_headers
#                 if header not in headers
#             ]

#             if missing_headers:

#                 attendance_import.status = "failed"
#                 attendance_import.error_message = (
#                     "Missing columns: "
#                     + ", ".join(missing_headers)
#                 )
#                 attendance_import.save()

#                 return attendance_import

#             header_map = {
#                 header: index
#                 for index, header in enumerate(headers)
#             }

#             total = 0
#             success = 0
#             failed = 0

#             for row_number, row in enumerate(
#                 rows[1:],
#                 start=2
#             ):

#                 total += 1

#                 employee_code = row[
#                     header_map["employee_code"]
#                 ]

#                 attendance_date = row[
#                     header_map["date"]
#                 ]

#                 in_time = row[
#                     header_map["in_time"]
#                 ]

#                 out_time = row[
#                     header_map["out_time"]
#                 ]

#                 import_row = AttendanceImportRow.objects.create(
#                     attendance_import=attendance_import,
#                     row_number=row_number,
#                     employee_code=str(
#                         employee_code
#                     ).strip()
#                     if employee_code is not None
#                     else "",
#                 )

#                 try:

#                     if not employee_code:

#                         raise ValueError(
#                             "Employee code is required."
#                         )

#                     employee = Employee.objects.get(
#                         employee_code=str(
#                             employee_code
#                         ).strip(),
#                         company=attendance_import.company,
#                         plant=attendance_import.plant,
#                     )

#                     if not attendance_date:

#                         raise ValueError(
#                             "Attendance date is required."
#                         )

#                     if isinstance(
#                         attendance_date,
#                         datetime
#                     ):

#                         attendance_date = (
#                             attendance_date.date()
#                         )

#                     if isinstance(
#                         in_time,
#                         datetime
#                     ):
#                         in_time_datetime = in_time

#                     else:
#                         in_time_datetime = None

#                     if isinstance(
#                         out_time,
#                         datetime
#                     ):
#                         out_time_datetime = out_time

#                     else:
#                         out_time_datetime = None

#                     import_row.employee = employee
#                     import_row.attendance_date = (
#                         attendance_date
#                     )

#                     import_row.in_time = (
#                         in_time_datetime
#                     )

#                     import_row.out_time = (
#                         out_time_datetime
#                     )

#                     import_row.save()

#                     AttendanceService.create_or_update_attendance(
#                         employee=employee,
#                         attendance_date=attendance_date,
#                         in_time=in_time_datetime,
#                         out_time=out_time_datetime,
#                         source="excel"
#                     )

#                     import_row.status = "success"
#                     import_row.save(
#                         update_fields=["status"]
#                     )

#                     success += 1

#                 except Exception as exc:

#                     import_row.status = "failed"
#                     import_row.error_message = str(exc)

#                     import_row.save(
#                         update_fields=[
#                             "status",
#                             "error_message"
#                         ]
#                     )

#                     failed += 1

#             attendance_import.total_rows = total
#             attendance_import.successful_rows = success
#             attendance_import.failed_rows = failed

#             if failed == 0:

#                 attendance_import.status = "completed"

#             elif success > 0:

#                 attendance_import.status = (
#                     "partially_completed"
#                 )

#             else:

#                 attendance_import.status = "failed"

#             attendance_import.save()

#             return attendance_import

#         except Exception as exc:

#             attendance_import.status = "failed"
#             attendance_import.error_message = str(exc)

#             attendance_import.save()

#             return attendance_import

import re
import calendar

from datetime import datetime, date, time, timedelta

from django.db import transaction
from django.utils import timezone

from openpyxl import load_workbook

from apps.hrms.models.employee import Employee
from apps.hrms.models.attendance import Attendance
from apps.hrms.models.attendance_import_row import (
    AttendanceImportRow
)

from apps.hrms.services.attendance_service import (
    AttendanceService
)


class ExcelAttendanceService:

    # ============================================================
    # 1. FIND EMPLOYEE CODE FROM EXCEL EMPLOYEE ROW
    # ============================================================

    @staticmethod
    def _find_employee_code(row):
        """
        Find employee code from a row containing values such as:

            Employee:
            1 : SHANKAR BURANGE
            3 : GAJANAN GADGE
            25 : ABHIJEET PATIL

        Returns:
            Employee code as string
        """

        for value in row:

            if value is None:
                continue

            text = str(value).strip()

            if not text:
                continue

            match = re.search(
                r"(\d+)\s*:\s*(.+)",
                text
            )

            if match:

                employee_code = match.group(1)

                return employee_code

        return None

    # ============================================================
    # 2. PARSE EXCEL TIME
    # ============================================================

    @staticmethod
    def _parse_time(value):
        """
        Convert Excel time value into Python time object.

        Supports:
            - datetime
            - time
            - timedelta
            - strings: 08:36
            - strings: 08:36:00
            - strings: 08:36 AM
            - strings: 08:36:00 AM
        """

        if value is None:
            return None

        # --------------------------------------------------------
        # Excel datetime
        # --------------------------------------------------------

        if isinstance(value, datetime):

            return value.time()

        # --------------------------------------------------------
        # Python time
        # --------------------------------------------------------

        if isinstance(value, time):

            return value

        # --------------------------------------------------------
        # Excel timedelta
        # --------------------------------------------------------

        if isinstance(value, timedelta):

            total_seconds = int(
                value.total_seconds()
            ) % (24 * 60 * 60)

            hours = total_seconds // 3600

            minutes = (
                total_seconds % 3600
            ) // 60

            seconds = (
                total_seconds % 60
            )

            return time(
                hour=hours,
                minute=minutes,
                second=seconds
            )

        # --------------------------------------------------------
        # String value
        # --------------------------------------------------------

        text = str(value).strip()

        if not text:
            return None

        # --------------------------------------------------------
        # Normalize common Excel text
        # --------------------------------------------------------

        text = text.replace(".", ":")

        # --------------------------------------------------------
        # Supported formats
        # --------------------------------------------------------

        time_formats = (
            "%H:%M",
            "%H:%M:%S",
            "%I:%M %p",
            "%I:%M:%S %p",
            "%I:%M%p",
            "%I:%M:%S%p",
        )

        for time_format in time_formats:

            try:

                return datetime.strptime(
                    text,
                    time_format
                ).time()

            except ValueError:

                continue

        return None

    # ============================================================
    # 3. CREATE TIMEZONE-AWARE DATETIME
    # ============================================================

    @staticmethod
    def _make_datetime(
        attendance_date,
        time_value
    ):
        """
        Combine attendance date and Excel time
        into a timezone-aware datetime.
        """

        parsed_time = (
            ExcelAttendanceService._parse_time(
                time_value
            )
        )

        if parsed_time is None:

            return None

        combined = datetime.combine(
            attendance_date,
            parsed_time
        )

        if timezone.is_naive(combined):

            combined = timezone.make_aware(
                combined
            )

        return combined

    # ============================================================
    # 4. PROCESS ATTENDANCE EXCEL IMPORT
    # ============================================================

    @staticmethod
    @transaction.atomic
    def process_import(attendance_import):

        attendance_import.status = "processing"

        attendance_import.error_message = ""

        attendance_import.save(
            update_fields=[
                "status",
                "error_message"
            ]
        )

        try:

            # ====================================================
            # 1. VALIDATE MONTH AND YEAR
            # ====================================================

            month = attendance_import.month

            year = attendance_import.year

            if not month or not 1 <= int(month) <= 12:

                raise ValueError(
                    "Invalid attendance month."
                )

            if not year or not 1900 <= int(year) <= 2100:

                raise ValueError(
                    "Invalid attendance year."
                )

            month = int(month)

            year = int(year)

            days_in_month = calendar.monthrange(
                year,
                month
            )[1]

            # ====================================================
            # 2. OPEN EXCEL FILE
            # ====================================================

            workbook = load_workbook(
                attendance_import.file.path,
                data_only=True
            )

            worksheet = workbook.active

            rows = list(
                worksheet.iter_rows(
                    values_only=True
                )
            )

            if not rows:

                attendance_import.status = "failed"

                attendance_import.error_message = (
                    "Excel file is empty."
                )

                attendance_import.save()

                return attendance_import

            # ====================================================
            # 3. FIND DAYS ROW
            # ====================================================

            days_row_index = None

            day_columns = {}

            for row_index, row in enumerate(
                rows
            ):

                first_value = (
                    str(row[0]).strip().lower()
                    if row and row[0] is not None
                    else ""
                )

                if first_value == "days":

                    days_row_index = row_index

                    for column_index, value in enumerate(
                        row
                    ):

                        if value is None:
                            continue

                        text = str(value).strip()

                        # Examples:
                        #
                        # 1 W
                        # 2 Th
                        # 3 F
                        # 4 St
                        # etc.

                        match = re.match(
                            r"^(\d{1,2})\b",
                            text
                        )

                        if match:

                            day_number = int(
                                match.group(1)
                            )

                            if (
                                1
                                <= day_number
                                <= days_in_month
                            ):

                                day_columns[
                                    day_number
                                ] = column_index

                    break

            if days_row_index is None:

                raise ValueError(
                    "Could not find 'Days' row in Excel."
                )

            if not day_columns:

                raise ValueError(
                    "Could not find attendance day columns."
                )

            # ====================================================
            # 4. FIND EMPLOYEE BLOCKS
            # ====================================================

            employee_blocks = []

            for row_index, row in enumerate(
                rows
            ):

                first_value = (
                    str(row[0]).strip().lower()
                    if row and row[0] is not None
                    else ""
                )

                if first_value != "employee:":
                    continue

                employee_code = (
                    ExcelAttendanceService
                    ._find_employee_code(row)
                )

                if not employee_code:
                    continue

                employee_blocks.append(
                    (
                        row_index,
                        employee_code
                    )
                )

            if not employee_blocks:

                raise ValueError(
                    "No employee records found in Excel."
                )

            # ====================================================
            # 5. COUNTERS
            # ====================================================

            total = 0

            success = 0

            failed = 0

            import_row_number = 1

            # ====================================================
            # 6. PROCESS EVERY EMPLOYEE
            # ====================================================

            for (
                employee_row_index,
                employee_code
            ) in employee_blocks:

                # ------------------------------------------------
                # Employee block normally contains:
                #
                # Employee:
                # Status
                # in_time
                # out_time
                #
                # We search dynamically instead of assuming
                # fixed row positions.
                # ------------------------------------------------

                status_row = None

                in_time_row = None

                out_time_row = None

                for search_index in range(
                    employee_row_index + 1,
                    min(
                        employee_row_index + 10,
                        len(rows)
                    )
                ):

                    row = rows[search_index]

                    if not row:
                        continue

                    first_value = (
                        str(row[0]).strip().lower()
                        if row[0] is not None
                        else ""
                    )

                    if first_value == "status":

                        status_row = search_index

                    elif first_value == "in_time":

                        in_time_row = search_index

                    elif first_value == "out_time":

                        out_time_row = search_index

                # ------------------------------------------------
                # Fallback positions
                # ------------------------------------------------

                if in_time_row is None:

                    in_time_row = (
                        employee_row_index + 2
                    )

                if out_time_row is None:

                    out_time_row = (
                        employee_row_index + 3
                    )

                # =================================================
                # 7. FIND EMPLOYEE IN DATABASE
                # =================================================

                employee = None

                employee_lookup_error = None

                try:

                    employee = Employee.objects.get(
                        statutory__punching_code=str(
                            employee_code
                        ).strip(),
                        company=attendance_import.company,
                        plant=attendance_import.plant,
                    )

                except Employee.DoesNotExist:

                    employee_lookup_error = (
                        f"Punching code "
                        f"{employee_code} not found "
                        f"for selected company and plant."
                    )

                except Employee.MultipleObjectsReturned:

                    employee_lookup_error = (
                        f"Multiple employees found "
                        f"for punching code "
                        f"{employee_code}."
                    )

                # =================================================
                # 8. PROCESS EACH DAY
                # =================================================

                for (
                    day_number,
                    column_index
                ) in day_columns.items():

                    attendance_date = date(
                        year,
                        month,
                        day_number
                    )

                    # =================================================
                    # READ IN TIME
                    # =================================================

                    check_in_value = None

                    status_value = None

                    if (
                        status_row is not None
                        and status_row < len(rows)
                        and column_index < len(rows[status_row])
                    ):
                        status_value = rows[status_row][column_index]

                    cell_status = (
                        str(status_value).strip().upper()
                        if status_value is not None else ""
                    )
                    is_week_off = cell_status in ("WO", "WOP")

                    if (
                        in_time_row is not None
                        and in_time_row < len(rows)
                        and column_index < len(
                            rows[in_time_row]
                        )
                    ):

                        check_in_value = rows[
                            in_time_row
                        ][column_index]

                    # =================================================
                    # READ OUT TIME
                    # =================================================

                    check_out_value = None

                    if (
                        out_time_row is not None
                        and out_time_row < len(rows)
                        and column_index < len(
                            rows[out_time_row]
                        )
                    ):

                        check_out_value = rows[
                            out_time_row
                        ][column_index]

                    # =================================================
                    # CONVERT TO DATETIME
                    # =================================================

                    check_in_datetime = (
                        ExcelAttendanceService
                        ._make_datetime(
                            attendance_date,
                            check_in_value
                        )
                    )

                    check_out_datetime = (
                        ExcelAttendanceService
                        ._make_datetime(
                            attendance_date,
                            check_out_value
                        )
                    )

                    # =================================================
                    # CREATE IMPORT ROW
                    # =================================================

                    import_row = (
                        AttendanceImportRow.objects.create(
                            attendance_import=attendance_import,
                            row_number=import_row_number,
                            employee_code=str(
                                employee_code
                            ).strip(),
                            status="pending",
                            error_message=""
                        )
                    )

                    total += 1

                    import_row_number += 1

                    try:

                        # =============================================
                        # EMPLOYEE VALIDATION
                        # =============================================

                        if employee_lookup_error:

                            raise ValueError(
                                employee_lookup_error
                            )

                        if employee is None:

                            raise ValueError(
                                "Employee could not be found."
                            )

                        # =============================================
                        # SAVE IMPORT ROW
                        #
                        # IMPORTANT:
                        # Your AttendanceImportRow model uses:
                        #     in_time
                        #     out_time
                        #
                        # NOT:
                        #     check_in
                        #     check_out
                        # =============================================

                        import_row.employee = employee

                        import_row.attendance_date = (
                            attendance_date
                        )

                        import_row.in_time = (
                            check_in_datetime
                        )

                        import_row.out_time = (
                            check_out_datetime
                        )

                        import_row.save()

                        # =============================================
                        # CREATE / UPDATE ACTUAL ATTENDANCE
                        #
                        # AttendanceService can continue using
                        # check_in / check_out because these are the
                        # service method parameters.
                        # =============================================

                        AttendanceService.create_or_update_attendance(
                        employee=employee,
                        attendance_date=attendance_date,
                        in_time=check_in_datetime,
                        out_time=check_out_datetime,
                        source="excel"
                        )

                        if is_week_off:
                            attendance = Attendance.objects.get(
                                employee=employee,
                                attendance_date=attendance_date,
                            )
                            attendance.day_type = "week_off"
                            attendance.status = (
                                "present" if cell_status == "WOP" else "weekly_off"
                            )
                            attendance.save(update_fields=["day_type", "status", "updated_at"])
                        else:
                            Attendance.objects.filter(
                                employee=employee,
                                attendance_date=attendance_date,
                            ).update(day_type="working_day")

                        # =============================================
                        # MARK IMPORT ROW SUCCESS
                        # =============================================

                        import_row.status = "success"

                        import_row.error_message = ""

                        import_row.save(
                            update_fields=[
                                "status",
                                "error_message"
                            ]
                        )

                        success += 1

                    except Exception as exc:

                        # =============================================
                        # MARK IMPORT ROW FAILED
                        # =============================================

                        import_row.status = "failed"

                        import_row.error_message = str(
                            exc
                        )

                        import_row.save(
                            update_fields=[
                                "status",
                                "error_message"
                            ]
                        )

                        failed += 1

            # ====================================================
            # 9. UPDATE IMPORT SUMMARY
            # ====================================================

            attendance_import.total_rows = total

            attendance_import.successful_rows = success

            attendance_import.failed_rows = failed

            # ----------------------------------------------------
            # ALL SUCCESS
            # ----------------------------------------------------

            if failed == 0 and success > 0:

                attendance_import.status = "completed"

                attendance_import.error_message = ""

            # ----------------------------------------------------
            # PARTIAL SUCCESS
            # ----------------------------------------------------

            elif success > 0 and failed > 0:

                attendance_import.status = (
                    "partially_completed"
                )

                attendance_import.error_message = (
                    f"{failed} attendance rows failed."
                )

            # ----------------------------------------------------
            # ALL FAILED
            # ----------------------------------------------------

            else:

                attendance_import.status = "failed"

                attendance_import.error_message = (
                    "No attendance rows were imported."
                )

            attendance_import.save()

            return attendance_import

        # ========================================================
        # OUTER IMPORT ERROR
        # ========================================================

        except Exception as exc:

            attendance_import.status = "failed"

            attendance_import.error_message = str(
                exc
            )

            attendance_import.save()

            return attendance_import
