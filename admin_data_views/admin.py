from django.contrib import admin
from django.http import HttpRequest
from django.template.response import TemplateResponse
from django.urls import URLPattern, URLResolver, path
from django.utils.translation import gettext

from .settings import admin_data_settings
from .typing import Any, AppDict, AppModel, Callable, List, Union


__all__ = [
    "add_url",
    "get_data_admin_views",
]


def add_url(baseroute: str, route: str, name: str) -> AppModel:
    return {
        "name": " ".join([val.capitalize() for val in name.split("_")]),
        "object_name": name.lower(),
        "perms": {"add": False, "change": False, "delete": False, "view": True},
        "admin_url": f"/admin/{baseroute}/{route}/",
        "add_url": None,
        "view_only": True,
    }


def get_data_admin_views() -> AppDict:
    baseroute = admin_data_settings.NAME.lower().replace(" ", "-")
    return {
        "name": admin_data_settings.NAME,
        "app_label": baseroute,
        "app_url": f"/admin/{baseroute}/",
        "has_module_perms": True,
        "models": [
            add_url(baseroute=baseroute, route=item["route"], name=item["name"]) for item in admin_data_settings.URLS
        ],
    }


# Added to site


def get_app_list(self: admin.AdminSite, request: HttpRequest, *args) -> List[AppDict]:
    baseroute = admin_data_settings.NAME.lower().replace(" ", "-")
    app_dict = self._build_app_dict(request, *args) or {}  # pylint: disable=protected-access

    if baseroute not in app_dict and admin_data_settings.NAME in args:
        app_dict = {baseroute: app_dict}

    if not args or admin_data_settings.NAME in args:
        data_admin_views = get_data_admin_views()

        # Extend models in an already existing app
        if baseroute in app_dict and "models" in app_dict[baseroute]:
            app_dict[baseroute]["models"].extend(data_admin_views["models"])  # pragma: no cover
        else:
            app_dict[baseroute] = data_admin_views

    if admin_data_settings.NAME in args:
        app_dict = {baseroute: app_dict[baseroute]}

    # Sort the apps alphabetically.
    app_list = sorted(app_dict.values(), key=lambda x: x["name"].lower())

    # Sort the models alphabetically within each app.
    for app in app_list:
        app["models"].sort(key=lambda x: x["name"])

    return app_list


def admin_data_index_view(self: admin.AdminSite, request: HttpRequest, **kwargs: Any) -> TemplateResponse:
    app_list = self.get_app_list(request, admin_data_settings.NAME)
    context = {
        "title": gettext("%(app)s administration") % {"app": app_list[0]["name"]},
        "subtitle": None,
        "app_list": app_list,
        "app_label": admin_data_settings.NAME,
    }
    context.update(self.each_context(request))
    context.update(kwargs.get("extra_context", {}))

    request.current_app = admin_data_settings.NAME
    return TemplateResponse(request, "admin/app_index.html", context)


def get_admin_data_urls(self: admin.AdminSite) -> List[Union[URLResolver, URLPattern]]:
    baseroute = admin_data_settings.NAME.lower().replace(" ", "-")
    custom_paths = [
        path(
            route=f"{baseroute}/",
            view=self.admin_view(self.admin_data_index_view),
            name="admin-data-index-view",
        )
    ]
    for item in admin_data_settings.URLS:
        custom_paths.append(
            path(
                route=f"{baseroute}/{item['route']}/",
                view=self.admin_view(item["view"]),
                name=item["name"],
            )
        )
        if item["items"] is not None:
            custom_paths.append(
                path(
                    route=f"{baseroute}/{item['route']}/{item['items']['route']}/",
                    view=self.admin_view(item["items"]["view"]),
                    name=item["items"]["name"],
                )
            )

    return custom_paths


def get_urls(
    original_get_urls: Callable[[], List[Union[URLResolver, URLPattern]]],
) -> Callable[[admin.AdminSite], List[Union[URLResolver, URLPattern]]]:
    def get_urls_inner(self: admin.AdminSite) -> List[Union[URLResolver, URLPattern]]:
        return self.get_admin_data_urls() + original_get_urls()

    return get_urls_inner


# Patch the admin site object with data admin view methods
# pylint: disable=no-value-for-parameter
admin.site.get_app_list = get_app_list.__get__(admin.site, admin.AdminSite)
admin.site.admin_data_index_view = admin_data_index_view.__get__(admin.site, admin.AdminSite)
admin.site.get_admin_data_urls = get_admin_data_urls.__get__(admin.site, admin.AdminSite)
admin.site.get_urls = get_urls(admin.site.get_urls).__get__(admin.site, admin.AdminSite)
