from django.apps import AppConfig


__all__ = [
    "MyAppConfig",
]


class MyAppConfig(AppConfig):
    name = "tests.myapp"
    verbose_name = "myapp"
    default_auto_field = "django.db.models.BigAutoField"
