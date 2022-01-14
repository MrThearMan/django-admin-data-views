## Setup

① Add `admin_data_views` to installed apps after `django.contrib.admin`

```python
INSTALLED_APPS = [
    ...
    "django.contrib.admin",
    "admin_data_views",
    ...
]
```

> `django.contrib.admin` and its [dependencies][admin-deps] need to be installed for `admin_data_views` to work


② (Optional) Add any models that would otherwise be registered
in `django.contrib.admin.site` to `admin_data_views.admin.admin_site`

```python
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from admin_data_views.admin import admin_site


admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)
```


③ Create data functions

```python
from django.core.handlers.wsgi import WSGIRequest
from admin_data_views.typing import TableContext, ItemContext
from admin_data_views.utils import render_with_table_view, render_with_item_view, item_view_link

@render_with_table_view
def foo_list_view(request: WSGIRequest) -> TableContext:
    return TableContext(
        title="Foo items",
        subtitle=None,
        table={
            "Name": [item_view_link(link_text="Foo", view=foo_list_view, args=(123,)), "1"],
            "Value": [item_view_link(link_text="Bar", view=foo_list_view, args=(124,)), "2"],
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
```

`render_with_table_view` is used to render the data in a table view. The view takes a single argument `request`,
and must return a dictionary matching the `TableContext` TypedDict.

`render_with_item_view` is used to render the data in an item view. The view takes an argument `request` and any
number or path arguments, and must return a dictionary matching the `ItemContext` TypedDict.

`item_view_link` is used to add links for the rows in the table view to the items in the items view.
Note that it takes a reference of the table view, not the item view it is linking to!
The matching item view is determined from the configuration made in the next step.


④ Add configuration to project `settings.py`

```python
ADMIN_DATA_VIEWS = {
    "URLS": [
        {
            "route": "foo/",
            "view": "path.to.function.foo_list_view",
            "name": "foo_list",
            "items": {
                "route": "<int:idd>/",
                "view": "path.to.function.foo_items_view",
                "name": "foo_item",
            },
        },
    ]
}
```


⑤ Now the views should be available in the admin panel under the `ADMIN DATA VIEWS` section.


![Front page](img/frontpage.png)

![Data views](img/dataviews.png)

![Table views](img/tableview.png)

![Item view](img/itemview.png)


[admin-deps]: https://docs.djangoproject.com/en/dev/ref/contrib/admin/#overview
