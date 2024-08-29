import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example_project.project.settings")

django.setup()
