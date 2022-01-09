from django.contrib.admin import apps


__all__ = [
    "AdminConfig",
]


class AdminConfig(apps.AdminConfig):
    name = "admin_data_views"
    verbose_name = "Admin Data Views"
    default_site = "admin_data_views.admin.AdminSite"
