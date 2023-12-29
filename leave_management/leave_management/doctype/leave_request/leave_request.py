# Copyright (c) 2023, Fadil Siddique and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime

class LeaveRequest(Document):
	def validate(self):
		current_month = datetime.now().month
		next_month = (current_month % 12) + 1
		roles = frappe.get_roles(frappe.session.user)

		if 'Employee' in roles:

			leave_settings = frappe.get_doc('Leave Settings')
			restricted_dates = []

			for dates in leave_settings.restrict_leave:
				restricted_dates.append(dates.date2.strftime('%Y-%m-%d'))

			current_month_leave_balance, current_month_excuse_balance, designation, floor,next_month_leave_balance,next_month_excuse_balance = frappe.db.get_value(
				'Employee',
				self.employee,
				['current_month_leave_balance',
				'current_month_excuse_balance',
				'designation',
				'floor',
				'next_month_leave_balance',
				'next_month_excuse_balance'
				])
			if floor:
				floor_wise_leave(self,leave_settings)
			if designation:
				designation_wise_leave(self,leave_settings)

			if self.request_type == 'Leave':
				requests = frappe.db.count(self.doctype,{'from_date':self.from_date,'leave_status':['in',['Approved']]})

				if self.from_date in restricted_dates:
					frappe.throw(title="Request Denied", msg="Taking Leave On Selected Date Is Restricted By Management. Please Contact HR")


				if requests == leave_settings.maximum_leaves_per_day:
					frappe.throw("Maximum Leaves For Selected Date Is Taken, Please Contact HR")
				
				leave_date_str = self.from_date
				leave_date_object = datetime.strptime(leave_date_str, '%Y-%m-%d')
				leave_month_value = leave_date_object.month
				
				if leave_month_value == current_month and current_month_leave_balance == 0.0:
					frappe.throw('Maximum leave for this month is taken. Please contact HR for new request')
				
				if leave_month_value == next_month and next_month_leave_balance == 0.0:
					frappe.throw('Maximum leave for this month is taken. Please contact HR for new request')

			elif self.request_type == 'Excuse':

				requests = frappe.db.count(self.doctype,{'time':self.time,'leave_status':['in',['Approved']]})

				if self.time in restricted_dates:
					frappe.throw(title="Request Denied", msg="Taking Excuse On Selected Date Is Restricted By Management. Please Contact HR")
				if requests == leave_settings.maximum_excuses_per_day:
					frappe.throw ("Maximum Excuse For The Selected Date Is Taken, Please Contact HR")

				excuse_date_str = self.time
				excuse_date_object = datetime.strptime(excuse_date_str, '%Y-%m-%d')
				excuse_month_value = excuse_date_object.month

				if excuse_month_value == current_month and current_month_excuse_balance == 0.0:
					frappe.throw('Maximum excuse for this month is taken. Please contact HR for new request')
				if excuse_month_value == next_month and next_month_excuse_balance == 0.0:
					frappe.throw('Maximum excuse for this month is taken. Please contact HR for new request')

				
	def on_cancel(self):
		employee = frappe.get_doc('Employee',self.employee)

		if self.leave_status == 'Approved':
			if self.request_type == 'Leave':
				leave_balance=employee.current_month_leave_balance
				frappe.db.set_value('Employee',self.employee,'current_month_leave_balance',leave_balance + 1)
			if self.request_type == 'Excuse':
				excuse_balance = employee.current_month_excuse_balance
				frappe.db.set_value('Employee',self.employee,'current_month_excuse_balance',excuse_balance +1)
			
			frappe.db.set_value('Leave Request',self.name,'leave_status','Rejected')

	def on_update_after_submit(self):
		employee = frappe.get_doc('Employee',self.employee)

		if self.leave_status == 'Rejected':
			if self.request_type == 'Leave':
				leave_balance=employee.current_month_leave_balance
				frappe.db.set_value('Employee',self.employee,'current_month_leave_balance',leave_balance + 1)
			if self.request_type == 'Excuse':
				excuse_balance = employee.current_month_excuse_balance
				frappe.db.set_value('Employee',self.employee,'current_month_excuse_balance',excuse_balance +1)
	
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

	def after_insert(self):
		send_email_notification(self.name)

def floor_wise_leave(self,leave_settings):

		roles = frappe.get_roles(frappe.session.user)
		
		if not 'HR Manager' in roles or 'Asst. HR' in roles or 'System Manager' in roles:
		
			floor,request_type= self.floor,self.request_type
			leave_requests = frappe.db.count(self.doctype,{'from_date':self.from_date,'request_type':'Leave','leave_status':['in',['Approved']],'floor':floor})
			excuse_requests = frappe.db.count(self.doctype,{'time':self.time,'request_type':'Excuse','leave_status':['in',['Approved']],'floor':floor})

			if floor:
				for i in leave_settings.floor_leave_allocation_table:
					if i.floor == floor:
						if request_type == 'Leave':
							if leave_requests >= i.maximum_leaves:
								frappe.throw(f"Maximum Leaves For {floor} Floor Has Been Taken")
						if request_type == 'Excuse':
							if excuse_requests >= i.maximum_leaves:
								frappe.throw(f"Maximum Excuses For {floor} Floor Has Been Taken")

def designation_wise_leave(self,leave_settings):

		roles = frappe.get_roles(frappe.session.user)
		
		if not 'HR Manager' in roles or 'Asst. HR' in roles or 'System Manager' in roles:
			designation, request_type= self.designation, self.request_type
			leave_requests = frappe.db.count(self.doctype,{'from_date':self.from_date,'request_type':'Leave','leave_status':['in',['Approved']],'designation':designation})
			excuse_requests = frappe.db.count(self.doctype,{'time':self.time,'request_type':'Excuse','leave_status':['in',['Approved']],'designation':designation})


			if designation:
				for i in leave_settings.designation_leave_allocation_table:
					if i.designation == designation:
						if request_type == 'Leave':
							if leave_requests >= i.maximum_leaves:
								frappe.throw(f"Maximum Leaves For {designation} Role Has Been Taken")

						if request_type == 'Excuse':
							if excuse_requests>= i.maximum_leaves:
								frappe.throw(f"Maximum Excuses For {designation} Role Has Been Taken")



def send_email_notification(docname):

	doc = frappe.get_doc('Leave Request', docname)
	subject = f"New {doc.request_type} Request From {doc.name1}"
	message = f"A new leave request has been submitted by {doc.name1}.\n"
	message += f"Link to Leave Request: {frappe.utils.get_url_to_form('Leave Request', docname)}"

	frappe.sendmail(
		recipients=['teamhr.mjr@gmail.com'],
		subject = subject,
		message = message
	)
			







