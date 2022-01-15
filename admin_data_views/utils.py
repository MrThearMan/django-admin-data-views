from functools import wraps
from typing import Any, Callable, List

from django.core.handlers.wsgi import WSGIRequest
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
    func: Callable[[WSGIRequest], TableContext],
) -> Callable[[WSGIRequest], TemplateResponse]:
    """Render returned context in a table view."""

    @wraps(func)
    def wrapper(request: WSGIRequest) -> TemplateResponse:
        context = func(request)
        func_name = f"{func.__module__}.{func.__qualname__}"  # noqa

        urls: List[URLConfig] = admin_data_settings.URLS
        for item in urls:
            view_name = f"{item['view'].__module__}.{item['view'].__qualname__}"
            if view_name == func_name:
                context["slug"] = item["route"]  # type: ignore

                # Look for any item links in the rows
                if item["items"] is not None:
                    item_view_name = item["items"]["name"]
                    for row in context["table"].values():
                        first_item = row[0]

                        if isinstance(first_item, ItemLink):
                            row[0] = format_html(
                                '<a href="{}">{}</a>',
                                reverse(
                                    viewname=f"admin:{item_view_name}",
                                    kwargs=first_item.kwargs,
                                    current_app=admin_site.name,
                                ),
                                str(first_item.link_item),
                            )
                break

        else:
            raise ValueError(f"Cannot find '{func_name}' in ADMIN_DATA_VIEWS setting.")

        context.update(admin_site.each_context(request))
        context["app_label"] = AdminConfig.verbose_name  # type: ignore
        request.current_app = admin_site.name
        return TemplateResponse(request, "admin_data_views/admin_data_table_page.html", context)

    return wrapper


def render_with_item_view(
    func: Callable[[WSGIRequest, ...], ItemContext],
) -> Callable[[WSGIRequest, ...], TemplateResponse]:
    """Render returned context in an item view."""

    @wraps(func)
    def wrapper(*args, **kwargs) -> TemplateResponse:
        request: WSGIRequest = args[0]
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

    def __str__(self) -> str:
        return str(self.link_item)
