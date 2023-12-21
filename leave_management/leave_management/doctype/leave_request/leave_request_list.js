frappe.listview_settings['Leave Request'] = {
    
    onload(listView){
        var userRoles = frappe.user_roles

        console.log(userRoles)

        if (userRoles.includes('Floor Manager') && !userRoles.includes('Administrator')){
            
            listView.$page.find(`div[class='filter-selector']`).css('display','none')
            listView.$page.find('.custom-actions, .hidden-xs, .hidden-md').css('display','none')

        }
    }
}