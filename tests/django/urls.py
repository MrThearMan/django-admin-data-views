from contextlib import suppress

from django.contrib import admin
from django.contrib.auth.models import User
from django.core.management import call_command
from django.http import HttpRequest
from django.urls import path

from admin_data_views.typing import ItemContext, TableContext
from admin_data_views.utils import ItemLink, render_with_item_view, render_with_table_view


with suppress(Exception):
    call_command("makemigrations")
    call_command("migrate")
    if not User.objects.filter(username="x", email="user@user.com").exists():
        User.objects.create_superuser(username="x", email="user@user.com", password="x")


@render_with_table_view
def foo_list_view(request: HttpRequest) -> TableContext:
    return TableContext(
        title="Foo items",
        subtitle=None,
        table={
            "Name": [ItemLink("Foo", idd=123), ItemLink("Bar", idd=124)],
            "Value": ["1", "2"],
        },
    )


@render_with_item_view
def foo_items_view(request: HttpRequest, idd: int) -> ItemContext:
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
def bar_list_view(request: HttpRequest) -> TableContext:
    return TableContext(
        title="Bar items",
        subtitle=None,
        table={
            "Fizz": [ItemLink("X"), ItemLink("Y")],
            "Buzz": ["1", "2"],
        },
    )


@render_with_item_view
def bar_items_view(request: HttpRequest) -> ItemContext:
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
def fizz_view(request: HttpRequest) -> TableContext:
    return TableContext(
        title="Fizz view",
        subtitle=None,
        table={
            "A": ["X", "Y"],
            "B": ["1", "2"],
        },
    )


@render_with_item_view
def buzz_view(request: HttpRequest) -> ItemContext:
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


urlpatterns = [path("admin/", admin.site.urls)]
