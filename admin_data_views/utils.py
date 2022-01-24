from functools import wraps
from typing import Any, Callable, List

from django.http import HttpRequest
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.html import format_html

from .admin import admin_site
from .apps import AdminConfig
from .settings import admin_data_settings
from .typing import ItemContext, TableContext, URLConfig


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
        request: HttpRequest = args[0]
        context = func(*args, **kwargs)
        func_name = f"{func.__module__}.{func.__qualname__}"  # noqa
        urls: List[URLConfig] = admin_data_settings.URLS

        for item in urls:  # pylint: disable=R1702:
            view_name = f"{item['view'].__module__}.{item['view'].__qualname__}"
            if view_name == func_name:
                context["slug"] = item["route"]  # type: ignore

                # Look for any item links in the rows.
                if item["items"] is not None:
                    item_view_name = item["items"]["name"]

                    for header in context["table"]:
                        for row_no, cell in enumerate(context["table"][header]):
                            if not isinstance(cell, ItemLink):  # pragma: no cover
                                continue

                            context["table"][header][row_no] = format_html(  # type: ignore
                                '<a href="{}">{}</a>',
                                reverse(
                                    viewname=f"admin:{item_view_name}",
                                    kwargs=cell.kwargs,
                                    current_app=admin_site.name,
                                ),
                                str(cell.link_item),
                            )

                        break  # Only the first column
                break  # Stop searching once view is found

        else:
            raise ValueError(f"Cannot find '{func_name}' in ADMIN_DATA_VIEWS setting.")

        # Transform the columns into a list of rows.
        # This way the table is easier to render in the template.
        context["headers"] = list(context["table"].keys())  # type: ignore
        context["rows"]: List[List[Any]] = [[] for _ in next(iter(context["table"].values()))]  # type: ignore
        for column in context["table"].values():
            for row_no, cell in enumerate(column):
                context["rows"][row_no].append(cell)  # type: ignore

        context.update(admin_site.each_context(request))
        context["app_label"] = AdminConfig.verbose_name  # type: ignore
        request.current_app = admin_site.name
        return TemplateResponse(request, "admin_data_views/admin_data_table_page.html", context)

    return wrapper


def render_with_item_view(
    func: Callable[..., ItemContext],
) -> Callable[..., TemplateResponse]:
    """Render returned context in an item view."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> TemplateResponse:
        request: HttpRequest = args[0]
        context = func(*args, **kwargs)
        func_name = f"{func.__module__}.{func.__qualname__}"  # noqa

        for item in admin_data_settings.URLS:
            # Allow item views separately
            view_name = f"{item['view'].__module__}.{item['view'].__qualname__}"
            if view_name == func_name:
                if context.get("slug") is None:
                    context["slug"] = item["route"]  # type: ignore
                break

            # Item view inside table view definition
            if item["items"] is not None:
                view_name = f"{item['items']['view'].__module__}.{item['items']['view'].__qualname__}"
                if view_name == func_name:
                    if context.get("slug") is None:
                        context["slug"] = item["items"]["route"]  # type: ignore
                    context["category_slug"] = item["route"]  # type: ignore
                    context["category_url"] = reverse(  # type: ignore
                        viewname=f"admin:{item['name']}",
                        current_app=admin_site.name,
                    )
                    break
        else:
            raise ValueError(f"Cannot find '{func_name}' in ADMIN_DATA_VIEWS setting.")

        context.update(admin_site.each_context(request))
        context["app_label"] = AdminConfig.verbose_name  # type: ignore
        request.current_app = admin_site.name
        return TemplateResponse(request, "admin_data_views/admin_data_item_page.html", context)

    return wrapper


class ItemLink:
    def __init__(self, link_item: Any, /, **kwargs: Any):
        """Marks a link to an item for the given view.

        :param link_item: Link text.
        :param args: Additional arguments to pass to the item route.
        """
        self.link_item = link_item
        self.kwargs = kwargs
