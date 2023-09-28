# Copyright (c) 2023, Fadil Siddique and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Employee(Document):
	
	def after_insert(self):

		leave_settings = frappe.get_doc('Leave Settings')
		self.current_month_leave_balance = leave_settings.maximum_leaves_per_month
		self.current_month_excuse_balance = leave_settings.maximum_excuses_per_month

		self.save()

		if self.user_details:

			doc = frappe.get_doc({
				'doctype': 'User Permission',
				'user': self.user_details,
				'allow':'Employee',
				'for_value': self.name
				})

			doc.insert()

		else:
			frappe.throw('Enter username of employee in user details')

