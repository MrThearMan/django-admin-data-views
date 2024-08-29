from django.contrib import admin

from example_project.myapp.models import Thing


@admin.register(Thing)
class AdminThing(admin.ModelAdmin):
    pass
