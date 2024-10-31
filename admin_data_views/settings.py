from __future__ import annotations

from django.test.signals import setting_changed
from settings_holder import SettingsHolder, reload_settings

from .typing import Any, NamedTuple, URLConfig

__all__ = [
    "admin_data_settings",
]


class AdminDataViewsSettings(NamedTuple):
    #
    # URLs for top-level categories. These will appear in the sidebar.
    # URLs for item pages. These will not appear in the sidebar.
    URLS: list[URLConfig] = []
    #
    # Name of the admin data views section in admin panel
    NAME: str = "Admin Data Views"


SETTING_NAME = "ADMIN_DATA_VIEWS"

DEFAULTS: dict[str, Any] = AdminDataViewsSettings()._asdict()


IMPORT_STRINGS: set[bytes | str] = {
    "URLS.0.view",
    "URLS.0.items.view",
}

REMOVED_SETTINGS: set[str] = set()


def urls_validator(val: Any) -> None:
    if not isinstance(val, list):  # pragma: no cover
        msg = "URLS must be a list"
        raise TypeError(msg)

    for i, item in enumerate(val):
        if not isinstance(item, dict):  # pragma: no cover
            msg = f"URLS[{i}] must be a dict"
            raise TypeError(msg)

        missing = {"route", "view", "name"}.difference(item.keys())
        if missing:
            msg = f"Missing keys in URLS[{i}]: {missing}"
            raise TypeError(msg)

        item["route"] = item["route"].rstrip("/").lstrip("/")

        items = item.get("items")
        if items is None:
            continue

        if not isinstance(items, dict):  # pragma: no cover
            msg = f"URLS[{i}]['items'] must be a dict"
            raise TypeError(msg)

        missing = {"route", "view", "name"}.difference(items.keys())
        if missing:
            msg = f"Missing keys in URLS[{i}]['items']: {missing}"
            raise TypeError(msg)

        items["route"] = items["route"].rstrip("/").lstrip("/")


VALIDATORS: dict[str, Any] = {
    "URLS": urls_validator,
}

admin_data_settings = SettingsHolder(
    setting_name=SETTING_NAME,
    defaults=DEFAULTS,
    import_strings=IMPORT_STRINGS,
    removed_settings=REMOVED_SETTINGS,
    validators=VALIDATORS,
)

reload_admin_data_settings = reload_settings(SETTING_NAME, admin_data_settings)
setting_changed.connect(reload_admin_data_settings)
