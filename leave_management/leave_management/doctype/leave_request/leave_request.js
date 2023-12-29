// Copyright (c) 2023, Fadil Siddique and contributors
// For license information, please see license.txt

frappe.ui.form.on('Leave Request', {
	// refresh: function(frm) {

	// }

	validate: function(frm){
		if ( frappe.user.has_role("Employee")){
		console.log(frm.doc.request_type, frm.doc.excuse_type)

			if (frm.doc.request_type == 'Leave'){
				let selected_date = new Date(frm.doc.from_date);
				let day = selected_date.getDay();
				if (day === 5 || day === 6){
					frappe.throw('You Cannot Apply For Leave On Friday And Staurday. Please Contact HR.');
				}
		}
		if (frm.doc.request_type =='Excuse' && frm.doc.excuse_type == 'Evening'){
			let excuse_date = new Date(frm.doc.time);
			let excuse_day = excuse_date.getDay();
			if (excuse_day === 5 || excuse_day === 6){
				frappe.throw('You Cannot Apply For Evening Excuse On Friday And Staurday. Please Contact HR.');
			}
		}

		}
		
	}
});
