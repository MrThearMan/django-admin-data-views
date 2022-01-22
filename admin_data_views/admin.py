from typing import List

from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.template.response import TemplateResponse
from django.urls import URLResolver, path

from .apps import AdminConfig
from .settings import admin_data_settings
from .typing import AppDict, AppModel


__all__ = [
    "admin_site",
]


class AdminSite(admin.AdminSite):
    """Custom admin panel to add rooms and other information to it."""

    def get_urls(self) -> List[URLResolver]:
        custom_paths = [
            path(
                route=f"{self.name}/",
                view=self.admin_view(self.admin_data_index_view),
                name="admin-data-index-view",
            )
        ]
        for item in admin_data_settings.URLS:
            custom_paths.append(
                path(
                    route=f"{self.name}/{item['route']}/",
                    view=self.admin_view(item["view"]),
                    name=item["name"],
                )
            )
            if item["items"] is not None:
                custom_paths.append(
                    path(
                        route=f"{self.name}/{item['route']}/{item['items']['route']}/",
                        view=self.admin_view(item["items"]["view"]),
                        name=item["items"]["name"],
                    )
                )

        return custom_paths + super().get_urls()  # noqa

    def admin_data_index_view(self, request: WSGIRequest) -> TemplateResponse:
        app_dict = self.get_data_admin_views()
        # Sort the models alphabetically
        app_dict["models"].sort(key=lambda x: x["name"])

        context = {
            **self.each_context(request),
            "title": app_dict["name"],
            "subtitle": None,
            "app_list": [app_dict],
            "app_label": AdminConfig.verbose_name,
        }

        request.current_app = self.name
        return TemplateResponse(request, "admin/app_index.html", context)  # noqa

    def get_app_list(self, request: WSGIRequest) -> List[AppDict]:
        app_dict = self._build_app_dict(request)
        app_dict[self.name] = self.get_data_admin_views()
        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x["name"].lower())

        # Sort the models alphabetically within each app.
        for app in app_list:
            app["models"].sort(key=lambda x: x["name"])

        return app_list

    def add_url(self, route: str, name: str) -> AppModel:
        return {
            "name": " ".join([val.capitalize() for val in name.split("_")]),
            "object_name": name.lower(),
            "perms": {"add": False, "change": False, "delete": False, "view": True},
            "admin_url": f"/admin/{self.name}/{route}/",
            "add_url": None,
            "view_only": True,
        }

    def get_data_admin_views(self) -> AppDict:
        return {
            "name": AdminConfig.verbose_name,
            "app_label": self.name,
            "app_url": f"/admin/{self.name}/",
            "has_module_perms": True,
            "models": [self.add_url(route=item["route"], name=item["name"]) for item in admin_data_settings.URLS],
        }


admin_site = AdminSite(name=AdminConfig.name.replace("_", "-"))
