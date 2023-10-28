# Copyright (c) 2023, Fadil Siddique and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime

class LeaveRequest(Document):
	def validate(self):
		
		roles = frappe.get_roles(frappe.session.user)

		if 'Employee' in roles:
			leave_settings = frappe.get_doc('Leave Settings')
			current_month_leave_balance, current_month_excuse_balance, department, floor= frappe.db.get_value('Employee',self.employee,['current_month_leave_balance','current_month_excuse_balance','department','floor'])
			if floor:
				floor_wise_leave(self,leave_settings)
			if department:
				department_wise_leave(self,leave_settings)

			if self.request_type == 'Leave':

				requests = frappe.db.count(self.doctype,{'from_date':self.from_date,'leave_status':['in',['Approved','Pending']]})
				if self.from_date==leave_settings.restrict_leave:
					frappe.throw(title="Request Denied", msg="Taking Leave On Selected Date Is Restricted By Management. Please Contact HR")


				if requests == leave_settings.maximum_leaves_per_day:
					frappe.throw("Maximum Leaves For Selected Date Is Taken, Please Contact HR")

				if current_month_leave_balance == 0.0:
					frappe.throw('Maximum leave for this month is taken. Please contact HR for new request')

			elif self.request_type == 'Excuse':

				requests = frappe.db.count(self.doctype,{'time':self.time,'leave_status':['in',['Approved','Pending']]})

				if self.time==leave_settings.restrict_leave:
					frappe.throw(title="Request Denied", msg="Taking Excuse On Selected Date Is Restricted By Management. Please Contact HR")
				if requests == leave_settings.maximum_excuses_per_day:
					frappe.throw ("Maximum Excuse For The Selected Date Is Taken, Please Contact HR")

				if current_month_excuse_balance == 0.0:
					frappe.throw('Maximum excuse for this month is taken. Please contact HR for new request')


	def on_submit(self):

		now = datetime.now()
		leave_settings = frappe.get_doc('Leave Settings')
		employee_doc=frappe.get_doc('Employee',self.employee)

		if self.leave_status=='Approved':

			if self.request_type == 'Leave':

				if employee_doc.current_month_leave_balance ==0.0:
					employee_doc.db_set('current_month_excuse_balance',employee_doc.current_month_excuse_balance - 1)

				if employee_doc.current_month_leave_balance >0.0 and self.from_date.month==now.month:
					employee_doc.db_set('current_month_leave_balance',employee_doc.current_month_leave_balance - 1)
				
				elif employee_doc.next_month_leave_balance >0.0 and self.from_date.month!=now.month:
					employee_doc.db_set('next_month_leave_balance',employee_doc.next_month_leave_balance - 1)


			elif self.request_type == 'Excuse':
				if employee_doc.current_month_excuse_balance ==0.0:
					employee_doc.db_set('current_month_leave_balance',employee_doc.current_month_leave_balance - 1)
		
				if employee_doc.current_month_excuse_balance >0.0 and self.time.month==now.month:
					employee_doc.db_set('current_month_excuse_balance',employee_doc.current_month_excuse_balance - 1)

				elif employee_doc.next_month_excuse_balance >0.0 and self.time.month==now.month:
					employee_doc.db_set('next_month_excuse_balance',employee_doc.next_month_excuse_balance - 1)

def floor_wise_leave(self,leave_settings):

		roles = frappe.get_roles(frappe.session.user)
		
		if not 'HR Manager' in roles or 'Asst. HR' in roles or 'System Manager' in roles:
		
			floor= frappe.db.get_value('Employee',self.employee,['floor'])
			requests = frappe.db.count(self.doctype,{'from_date':self.from_date,'leave_status':['in',['Approved','Pending']],'floor':floor})

			if floor:
				for i in leave_settings.floor_leave_allocation_table:
					if i.floor == floor:

						if requests >= i.maximum_leaves :
							frappe.throw(f"Maximum Leaves For {floor} Floor Has Been Taken")
	
def department_wise_leave(self,leave_settings):

		roles = frappe.get_roles(frappe.session.user)
		
		if not 'HR Manager' in roles or 'Asst. HR' in roles or 'System Manager' in roles:
			department= frappe.db.get_value('Employee',self.employee,['department'])
			requests = frappe.db.count(self.doctype,{'from_date':self.from_date,'leave_status':['in',['Approved','Pending']],'department':department})

			if department:
				for i in leave_settings.department_leave_allocation_table:
					if i.department == department:
						if requests >= i.maximum_leaves:
							frappe.throw(f"Maximum Leaves For {department} Department Has Been Taken")

			







