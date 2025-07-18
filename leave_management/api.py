import frappe
from frappe.utils import getdate, flt
import json


@frappe.whitelist()
def queue_individual_incentive(data):
    if not isinstance(data, list):
        data = [data]

    frappe.enqueue(
        method=process_individual_incentive,
        queue='default',
        timeout=600,
        job_name='Process Individual Incentive Entries',
        data=data
    )
    return "Task queued successfully"


@frappe.whitelist()
def process_individual_incentive(data):
    data = json.loads(data) if isinstance(data, str) else data

    for item in data:
        try:
            incentive_type = item.get("incentive_type")
            if incentive_type == "Gold Incentive":
                gold_incentive(item)
        except Exception as e:
            frappe.log_error(f"Error processing incentive for {item.get('employee')}: {str(e)}")
    return "Process Queued Successfully"


def get_present_employees(date, departments):
    date = getdate(date)
    departments = [departments] if isinstance(departments, str) else departments

    placeholders = ", ".join(["%s"] * len(departments))
    query = f"""
        SELECT emp.department, COUNT(att.name) AS count
        FROM `tabAttendance` att
        JOIN `tabEmployee` emp ON att.employee = emp.name
        WHERE
            att.attendance_date = %s
            AND att.status = 'Present'
            AND att.docstatus = 1
            AND emp.department IN ({placeholders})
        GROUP BY emp.department
    """
    results = frappe.db.sql(query, [date] + departments, as_dict=True)
    print(results)
    return {row['department']: row['count'] for row in results}


def get_attendance_map(date):
    """Returns a set of employee names marked present on a given date"""
    date = getdate(date)
    records = frappe.get_all("Attendance", filters={
        "attendance_date": date,
        "status": "Present",
        "docstatus": 1
    }, fields=["employee"])
    print(set(rec["employee"] for rec in records),"nadddidiididhshs")
    return set(rec["employee"] for rec in records)


def gold_incentive(data):
    # loc=get_attendance_map()
    from_date = getdate(data.get("date"))
    loc=get_attendance_map(from_date)
    print(loc,"hello")
    grams_sold = flt(data.get("metric_value"))
    employee_id = data.get("employee")
    parent_doc = data.get("parent")

    if not grams_sold:
        return

    rule = frappe.get_doc("MJ Incentive Rule", "Gold Incentive")
    weekday = from_date.weekday()
    threshold = rule.weekend_threshold if weekday == 6 else rule.weekday_threshold

    if grams_sold < threshold:
        return

    employee_dept = frappe.db.get_value("Employee", employee_id, "department")
    eligible_depts = [d.department for d in rule.eligible_department]
    qualified_depts = [d for d in eligible_depts if d != "Sales"]

    attendance_counts = get_present_employees(from_date, ["Sales"] + qualified_depts)
    total_sales = attendance_counts.get("Sales", 0)
    total_qualified = sum(attendance_counts.get(d, 0) for d in qualified_depts)

    denominator = total_sales + (total_qualified / 2)
    if denominator == 0:
        return

    incentive_common = (grams_sold * 2) / denominator
    attendance_map = get_attendance_map(from_date)

    if employee_dept == "Sales":
        create_incentive_entries(
            departments=[employee_dept],
            incentive_type="Individual",
            amount=incentive_common,
            date=from_date,
            incentive_name="Gold Incentive",
            parent_doc=parent_doc,
            attendance_map=attendance_map
            
        )

    if qualified_depts:
        create_incentive_entries(
            departments=qualified_depts,
            incentive_type="Department",
            amount=incentive_common / 2,
            date=from_date,
            incentive_name="Gold Incentive",
            parent_doc=parent_doc,
            attendance_map=attendance_map
            
        )

def diamond_incentive(data):
    from_date = getdate(data.get("date"))
    loc=get_attendance_map(from_date)
    print(loc,"hello")
    sales_amount = flt(data.get("metric_value"))
    employee_id = data.get("employee")
    parent_doc = data.get("parent")

    employee_dept = frappe.db.get_value("Employee", employee_id, "department")
    eligible_depts = [d.department for d in rule.eligible_department]
    qualified_depts = [d for d in eligible_depts if d != "Sales"]

    attendance_counts = get_present_employees(from_date, ["Sales"] + qualified_depts)
    total_sales = attendance_counts.get("Sales", 0)
    total_qualified = sum(attendance_counts.get(d, 0) for d in qualified_depts)
    attendance_map = get_attendance_map(from_date)


    if not sales_amount:
        return
    rule = frappe.get_doc("MJ Incentive Rule", "Gold Incentive")
    incentive_methood = rule.individual_calction_method
    individual_incentive_rate = rule.incentive_rate
    incentive_basis = rule.incentive_basis
    common_incentive_rate = rule.common_rate
    if rule.has_individual_incentive:
        individual_incentive_amount = (individual_incentive_rate*100)/sales_amount
        create_incentive_entries(
            departments=[employee_dept],
            incentive_type="Individual",
            amount=individual_incentive_amount,
            date=from_date,
            incentive_name="Diamond Incentive",
            parent_doc=parent_doc,
            attendance_map=attendance_map
            
        )
    if rule.has_common_incentive:
        common_incentive_amount = (common_incentive_rate*100)/sales_amount
        create_incentive_entries(
            departments=[employee_dept],
            incentive_type="Common",
            amount=common_incentive_amount,
            date=from_date,
            incentive_name="Diamond Incentive",
            parent_doc=parent_doc,
            attendance_map=attendance_map
        )

    if qualified_depts:
        individual_incentive_amount = (individual_incentive_rate*100)/sales_amount
        dept_incentive = individual_incentive_amount*2
        create_incentive_entries(
            departments=qualified_depts,
            incentive_type="Department",
            amount=dept_incentive,
            date=from_date,
            incentive_name="Diamond Incentive",
            parent_doc=parent_doc,
            attendance_map=attendance_map
            
        )
    
    

def create_incentive_entries(departments, incentive_type, amount, date, incentive_name, parent_doc,attendance_map):
    employees = frappe.get_all(
        "Employee",
        filters={"department": ["in", departments]},
        fields=["name"]
    )


    for emp in employees:
        if emp["name"] in attendance_map:

            frappe.get_doc({
                "doctype": "Daily Incentive Log",
                "employee": emp.name,
                "is_common_incentive": 1 if incentive_type == "Common" else 0,
                "is_individual_incentive": 1 if incentive_type == "Individual" else 0,
                "eligible_department_incentive": 1 if incentive_type == "Department" else 0,
                "incentive_amount": amount,
                "date": date,
                "incentive_type": incentive_name,
                "linked_document": parent_doc
            }).insert(ignore_permissions=True)
