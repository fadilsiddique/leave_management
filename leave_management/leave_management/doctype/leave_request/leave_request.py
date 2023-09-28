# Copyright (c) 2023, Fadil Siddique and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LeaveRequest(Document):

	def validate(self):
		
		roles = frappe.get_roles(frappe.session.user)

		if 'Employee' in roles:
			employee_doc=frappe.get_doc('Employee',self.employee)
			if self.request_type == 'Leave':

				if employee_doc.current_month_leave_balance == 0.0:
					frappe.throw('Maximum leave for this month is taken. Please contact HR for new request')

			elif self.request_type == 'Excuse':
			
				if employee_doc.current_month_excuse_balance == 0.0:
					frappe.throw('Maximum excuse for this month is taken. Please contact HR for new request')


	def on_submit(self):

		if self.leave_status=='Approved':

			employee_doc=frappe.get_doc('Employee',self.employee)

			if self.request_type == 'Leave':
				if employee_doc.current_month_leave_balance >0.0:
					employee_doc.db_set('current_month_leave_balance',employee_doc.current_month_leave_balance - 1)
					

			elif self.request_type == 'Excuse':
				if employee_doc.current_month_leave_balance >0.0:
					employee_doc.db_set('current_month_excuse_balance',employee_doc.current_month_excuse_balance - 1)



				
			
			


