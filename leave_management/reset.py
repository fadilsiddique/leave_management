import frappe
import calendar
from datetime import datetime
def reset_days():
    current_month_sunday_count =len([1 for i in calendar.monthcalendar(datetime.now().year,datetime.now().month) if i[6] != 0])

    total_leave = current_month_sunday_count + 1

    leave_settings = frappe.get_doc('Leave Settings')

    leave_settings.db_set('maximum_leaves_per_month',total_leave)
    leave_settings.db_set('maximum_excuses_per_month',total_leave)

    employee_list = frappe.db.get_list('Employee',fields='name')

    for employee in employee_list:

        frappe.db.set_value('Employee',employee.name,{
            'current_month_leave_balance':employee.next_month_leave_balance,
            'current_month_excuse_balance':employee.next_month_excuse_balance,
            'next_month_leave_balance':get_next_month_sunday_count(),
            'next_month_excuse_balance':get_next_month_sunday_count()
        })
    

    leave_settings.save(ignore_permissions=True)

def get_next_month_sunday_count():
    now = datetime.now()
    next_month = now.month + 1 if now.month < 12 else 1
    next_year = now.year if now.month < 12 else now.year + 1

    next_month_calendar = calendar.monthcalendar(next_year, next_month)
    next_month_sunday_count = len([1 for week in next_month_calendar if week[-1] != 0])

    total_leave = next_month_sunday_count + 1

    return total_leave
