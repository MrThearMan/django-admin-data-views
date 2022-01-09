from django.contrib.auth.models import User
from django.core.management import call_command
from django.urls import path

from admin_data_views.admin import admin_site
from admin_data_views.typing import ItemContext, TableContext
from admin_data_views.utils import item_view_link, render_with_item_view, render_with_table_view


call_command("makemigrations")
call_command("migrate")


if not User.objects.filter(username="x", email="user@user.com").exists():
    User.objects.create_superuser(username="x", email="user@user.com", password="x")


admin_site.register(User)


@render_with_table_view
def custom_view1(request):
    return TableContext(
        title="Foo items",
        subtitle=None,
        headers=[
            "Name",
            "Value",
        ],
        rows=[
            [item_view_link(link_text="Foo", view=custom_view1, args=(123,)), "1"],
            [item_view_link(link_text="Bar", view=custom_view1, args=(124,)), "2"],
        ],
    )


@render_with_item_view
def custom_view2(request, idd):
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
            }
        ],
    )


@render_with_table_view
def custom_view3(request):
    return TableContext(
        title="Bar items",
        subtitle=None,
        headers=[
            "Fizz",
            "Buzz",
        ],
        rows=[
            [item_view_link(link_text="X", view=custom_view3), "1"],
            [item_view_link(link_text="Y", view=custom_view3), "2"],
        ],
    )


@render_with_item_view
def custom_view4(request):
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
            }
        ],
    )


@render_with_table_view
def custom_view5(request):
    return TableContext(
        title="Fizz Buzz items",
        subtitle=None,
        headers=[
            "A",
            "B",
        ],
        rows=[
            ["X", "1"],
            ["Y", "2"],
        ],
    )


@render_with_item_view
def custom_view6(request):
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
            }
        ],
    )


urlpatterns = [path("admin/", admin_site.urls)]
