from django.contrib import admin

from tests.myapp.models import Thing


@admin.register(Thing)
class AdminThing(admin.ModelAdmin):
    pass
