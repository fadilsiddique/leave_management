import frappe
import calendar
from datetime import datetime
def reset_days():
    current_month_sunday_count =len([1 for i in calendar.monthcalendar(datetime.now().year,datetime.now().month) if i[6] != 0])

    leave_settings = frappe.get_doc('Leave Settings')

    leave_settings.db_set('maximum_leaves_per_month',current_month_sunday_count)
    leave_settings.db_set('maximum_excuses_per_month',current_month_sunday_count)

    employee_list = frappe.db.get_list('Employee',fields='name')

    for employee in employee_list:
        emp_doc = frappe.get_doc('Employee', employee.name)
        emp_doc.current_month_leave_balance = current_month_sunday_count
        emp_doc.save(ignore_permissions=True)

    leave_settings.save(ignore_permissions=True)
