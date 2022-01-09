from django.utils.module_loading import autodiscover_modules

from .admin import admin_site
from .apps import AdminConfig


def autodiscover():
    autodiscover_modules(AdminConfig.name, register_to=admin_site)
