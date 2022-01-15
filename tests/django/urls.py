from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User
from django.core.handlers.wsgi import WSGIRequest
from django.core.management import call_command
from django.urls import path

from admin_data_views.admin import admin_site
from admin_data_views.typing import ItemContext, TableContext
from admin_data_views.utils import ItemLink, render_with_item_view, render_with_table_view


call_command("makemigrations")
call_command("migrate")


if not User.objects.filter(username="x", email="user@user.com").exists():
    User.objects.create_superuser(username="x", email="user@user.com", password="x")


admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)


@render_with_table_view
def foo_list_view(request: WSGIRequest) -> TableContext:
    return TableContext(
        title="Foo items",
        subtitle=None,
        table={
            "Name": [ItemLink("Foo", idd=123), "1"],
            "Value": [ItemLink("Bar", idd=124), "2"],
        },
    )


@render_with_item_view
def foo_items_view(request: WSGIRequest, idd: int) -> ItemContext:
    return ItemContext(
        slug=idd,
        title=f"This is {idd}",
        subtitle=None,
        image=None,
        data=[
            {
                "name": None,
                "description": None,
                "fields": {
                    "Foo": idd,
                },
            },
            {
                "name": "This is another section",
                "description": "This is the description for this section",
                "fields": {
                    "Fizz": idd * 2,
                },
            },
        ],
    )


@render_with_table_view
def bar_list_view(request: WSGIRequest) -> TableContext:
    return TableContext(
        title="Bar items",
        subtitle=None,
        table={
            "Fizz": [ItemLink("X"), "1"],
            "Buzz": [ItemLink("Y"), "2"],
        },
    )


@render_with_item_view
def bar_items_view(request: WSGIRequest) -> ItemContext:
    return ItemContext(
        slug=None,
        title=f"Bar page",
        subtitle=None,
        image=None,
        data=[
            {
                "name": None,
                "description": None,
                "fields": {
                    "Foo": "Bar",
                },
            },
            {
                "name": "This is another section",
                "description": "This is the description for this section",
                "fields": {
                    "Fizz": "Buzz",
                },
            },
        ],
    )


@render_with_table_view
def fizz_view(request: WSGIRequest) -> TableContext:
    return TableContext(
        title="Fizz view",
        subtitle=None,
        table={
            "A": ["X", "1"],
            "B": ["Y", "2"],
        },
    )


@render_with_item_view
def buzz_view(request: WSGIRequest) -> ItemContext:
    return ItemContext(
        slug=None,
        title=f"Buzz page",
        subtitle=None,
        image=None,
        data=[
            {
                "name": None,
                "description": None,
                "fields": {
                    "Foo": "Bar",
                },
            },
        ],
    )


urlpatterns = [path("admin/", admin_site.urls)]
