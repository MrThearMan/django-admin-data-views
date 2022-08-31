from functools import wraps

from django.contrib import admin
from django.http import HttpRequest
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.html import format_html

from .settings import admin_data_settings
from .typing import Any, Callable, ItemContext, ItemViewContext, TableContext, TableViewContext, URLConfig


__all__ = [
    "render_with_item_view",
    "render_with_table_view",
    "ItemLink",
]


def render_with_table_view(
    func: Callable[..., TableContext],
) -> Callable[..., TemplateResponse]:
    """Render returned context in a table view."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> TemplateResponse:
        context = func(*args, **kwargs)
        func_name = f"{func.__module__}.{func.__qualname__}"

        item: URLConfig
        for item in admin_data_settings.URLS:
            view_name = f"{item['view'].__module__}.{item['view'].__qualname__}"
            if view_name == func_name:
                table_context = TableViewContext(
                    slug=item["route"],
                    title=context.get("title"),
                    subtitle=context.get("subtitle"),
                    app_label=admin_data_settings.NAME,
                    headers=list(context["table"].keys()),
                    rows=[],
                )

                # Transform the table columns into rows.
                # This way the table is easier to render in the template.
                for header in context["table"]:
                    for row_no, cell in enumerate(context["table"][header]):
                        if item["items"] is not None and isinstance(cell, ItemLink):
                            cell = format_html(
                                '<a href="{}">{}</a>',
                                reverse(
                                    viewname=f"admin:{item['items']['name']}",
                                    kwargs=cell.kwargs,
                                    current_app=admin_data_settings.NAME,
                                ),
                                str(cell.link_item),
                            )

                        if len(table_context["rows"]) <= row_no:
                            table_context["rows"].append([])

                        table_context["rows"][row_no].append(cell)

                break  # Stop searching once view is found
        else:
            raise ValueError(f"Cannot find '{func_name}' in ADMIN_DATA_VIEWS setting.")

        request: HttpRequest = args[0]
        table_context.update(admin.site.each_context(request))
        table_context = {**context.get("extra_context", {}), **table_context}
        request.current_app = admin_data_settings.NAME
        return TemplateResponse(request, "admin_data_views/admin_data_table_page.html", table_context)

    return wrapper


def render_with_item_view(
    func: Callable[..., ItemContext],
) -> Callable[..., TemplateResponse]:
    """Render returned context in an item view."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> TemplateResponse:
        context = func(*args, **kwargs)
        func_name = f"{func.__module__}.{func.__qualname__}"

        item_context = ItemViewContext(
            slug=context.get("slug"),
            title=context.get("title"),
            subtitle=context.get("subtitle"),
            image=context.get("image"),
            data=context.get("data"),
            app_label=admin_data_settings.NAME,
        )

        item: URLConfig
        for item in admin_data_settings.URLS:
            # Item views separately
            view_name = f"{item['view'].__module__}.{item['view'].__qualname__}"
            if view_name == func_name:
                if item_context["slug"] is None:
                    item_context["slug"] = item["route"]
                break  # Stop searching once view is found

            if item["items"] is None:
                continue

            # Item view inside table view definition
            view_name = f"{item['items']['view'].__module__}.{item['items']['view'].__qualname__}"
            if view_name == func_name:
                if item_context["slug"] is None:
                    item_context["slug"] = item["route"]
                item_context["category_slug"] = item["route"]
                item_context["category_url"] = reverse(
                    viewname=f"admin:{item['name']}",
                    current_app=admin_data_settings.NAME,
                )
                break  # Stop searching once view is found
        else:
            raise ValueError(f"Cannot find '{func_name}' in ADMIN_DATA_VIEWS setting.")

        request: HttpRequest = args[0]
        item_context.update(admin.site.each_context(request))
        item_context = {**context.get("extra_context", {}), **item_context}
        request.current_app = admin_data_settings.NAME
        return TemplateResponse(request, "admin_data_views/admin_data_item_page.html", item_context)

    return wrapper


class ItemLink:
    def __init__(self, link_item: Any, /, **kwargs: Any):
        """Marks a link to an item for the given view.

        :param link_item: Link text.
        :param args: Additional arguments to pass to the item route.
        """
        self.link_item = link_item
        self.kwargs = kwargs
