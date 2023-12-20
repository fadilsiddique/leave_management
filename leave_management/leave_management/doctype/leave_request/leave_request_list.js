frappe.listview_settings['Leave Request'] = {
    
    onload(listView){
        var userRoles = frappe.user_roles

        if (userRoles.includes('Floor Manager')){
            listView.$page.find(`div[class='filter-selector']`).addClass('hide')
        }
    }
}