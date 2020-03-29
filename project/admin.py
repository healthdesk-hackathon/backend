from django.contrib.admin import AdminSite as BaseAdminSite


class AdminSite(BaseAdminSite):
    site_header = 'Healthdesk Administration'
    site_title = 'Healthdesk'

admin_site = AdminSite()
