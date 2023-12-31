// Copyright (c) 2023, Fadil Siddique and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee', {
	// refresh: function(frm) {

	// }

	before_save: function(frm){

		let first_name = frm.doc.first_name
		let last_name = frm.doc.last_name
		let middle_name = frm.doc.middle_name

		let full_name = ''

		if (!middle_name && !last_name){
			full_name = first_name

			frm.set_value('full_name', full_name)
		}

		if(middle_name && !last_name){
			full_name = first_name.concat(" ",middle_name)

			frm.set_value('full_name', full_name)

		}

		if(!middle_name && last_name){
			full_name = first_name.concat(" ",last_name)

			frm.set_value('full_name', full_name)

		}

		if (middle_name && last_name){
			full_name = first_name.concat(" ",middle_name," ",last_name)

			frm.set_value('full_name', full_name)

		}

		


	},
	user_details: function(frm){

		frappe.db.get_doc('User',frm.doc.user_details).then( e=>{
			
			frm.set_value({
				'first_name':e.first_name,
				'middle_name':e.middle_name,
				'last_name':e.last_name,
				'gender':e.gender,
				'phone_no':e.mobile_no,

			})
		}
		)

		
	}
});
