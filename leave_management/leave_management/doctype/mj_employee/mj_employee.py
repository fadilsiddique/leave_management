# Copyright (c) 2023, Fadil Siddique and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from leave_management.reset import get_next_month_sunday_count

class MJEmployee(Document):
	
	def after_insert(self):

		leave_settings = frappe.get_doc('MJ Leave Settings')
		self.current_month_leave_balance = leave_settings.maximum_leaves_per_month
		self.current_month_excuse_balance = leave_settings.maximum_excuses_per_month
		self.next_month_leave_balance = get_next_month_sunday_count()
		self.next_month_excuse_balance = get_next_month_sunday_count()

		self.save()

		if self.user_details:

			doc = frappe.get_doc({
				'doctype': 'User Permission',
				'user': self.user_details,
				'allow':'MJ Employee',
				'for_value': self.name
				})

			doc.insert()

		else:
			frappe.throw('Enter user linked to current mj_employee in user details')

		# emp_list = frappe.get_list('MJEmployee',fields=['mj_employee_id'])
		# mj_employee_ids = [item["mj_employee_id"] for item in emp_list]
		# max_mj_employee_id = max(mj_employee_ids)

		# self.mj_employee_id = max_mj_employee_id + 1

		# self.save()

	def on_update(self):

		if self.status == 'Inactive':

			user = frappe.get_doc('User',self.user_details)

			user.enabled = 0

			user.db_set('enabled',0)





