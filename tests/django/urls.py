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


@render_with_item_view
def complex_view(request: HttpRequest) -> ItemContext:
    return ItemContext(
        slug="complex",
        title="This is complex",
        image="https://images.pexels.com/photos/355508/pexels-photo-355508.jpeg",
        data=[
            {
                "name": None,
                "description": None,
                "fields": {
                    "foo": "bar",
                    "list": ["bar", 1],
                    "title": {
                        "plain": "Send Money",
                    },
                    "fieldset": [
                        {
                            "label": {
                                "plain": "Personal Info Section",
                            },
                            "fieldset": [
                                {
                                    "field": [
                                        {
                                            "label": {
                                                "plain": "First Name",
                                            },
                                            "value": {
                                                "plain": "Bob",
                                            },
                                            "id": "a_1",
                                        },
                                        {
                                            "label": {
                                                "plain": "Last Name",
                                            },
                                            "value": {
                                                "plain": "Hogan",
                                            },
                                            "id": "a_2",
                                        },
                                    ],
                                    "id": "a_8",
                                }
                            ],
                            "id": "a_5",
                        },
                        {
                            "label": {
                                "plain": "Billing Details Section",
                            },
                            "fieldset": {
                                "field": {
                                    "choices": {
                                        "choice": {
                                            "label": {
                                                "plain": "Gift",
                                            },
                                            "id": "a_17",
                                            "switch": "",
                                        },
                                    },
                                    "label": {
                                        "plain": "Choose a category:",
                                    },
                                    "value": {
                                        "plain": "Gift",
                                    },
                                    "id": "a_14",
                                },
                                "fieldset": {
                                    "label": {
                                        "plain": "",
                                    },
                                    "field": [
                                        {
                                            "choices": {
                                                "choice": {
                                                    "label": {
                                                        "plain": "Other",
                                                    },
                                                    "id": "a_25",
                                                    "switch": "",
                                                }
                                            },
                                            "label": {
                                                "plain": "Amount",
                                            },
                                            "value": {
                                                "plain": "Other",
                                            },
                                            "id": "a_21",
                                        },
                                        {
                                            "label": {
                                                "plain": "Other Amount",
                                            },
                                            "value": {
                                                "plain": "200",
                                            },
                                            "id": "a_20",
                                        },
                                    ],
                                    "id": "a_26",
                                },
                                "id": "a_13",
                            },
                            "id": "a_12",
                        },
                    ],
                },
                "help_texts": {
                    "foo": "this is bar",
                    "list": "this is a list",
                    "title": {
                        "plain": "Plain title",
                    },
                    "fieldset": {
                        "label": {
                            "plain": "Plain label",
                        },
                        "fieldset": {
                            "field": "Fields",
                            "fieldset": "Nested Fieldsets",
                            "id": "Nested id",
                        },
                        "id": "First ID",
                    },
                },
            },
        ],
    )


urlpatterns = [path("admin/", admin.site.urls)]
