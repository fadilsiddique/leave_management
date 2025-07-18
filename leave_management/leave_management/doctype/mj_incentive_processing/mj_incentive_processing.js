// Copyright (c) 2025, Fadil Siddique and contributors
// For license information, please see license.txt

frappe.ui.form.on('MJ Incentive Processing', {
	refresh: function(frm) {
		frm.add_custom_button(__('Process Incentive'), function() {
			frappe.call({
				method: "leave_management.api.process_individual_incentive",
				args: {
					data: frm.doc.incentive_upload
				},
				callback: function(r) {
					if (r.message) {
						frappe.msgprint(__('Incentive processed successfully.'));
						frm.reload_doc();
					} else {
						frappe.msgprint(__('Failed to process incentive.'));
					}
				}
			});
			
		}, __("Action"));
	}
});
