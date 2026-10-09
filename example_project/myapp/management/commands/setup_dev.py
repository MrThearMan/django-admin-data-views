from typing import Any

from django.contrib.auth.models import User
from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = "Migrate the database and create the superuser for the development server."

    def handle(self, *args: Any, **options: Any) -> None:
        call_command("migrate")
        if not User.objects.filter(username="x").exists():
            User.objects.create_superuser(username="x", email="user@user.com", password="x")  # noqa: S106
            self.stdout.write("Created superuser 'x' with password 'x'.")
