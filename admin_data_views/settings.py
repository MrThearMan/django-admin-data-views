from django.test.signals import setting_changed
from settings_holder import holder, reload_settings

from .typing import Any, Dict, List, NamedTuple, Set, Union, URLConfig


__all__ = [
    "admin_data_settings",
]


class AdminDataViewsSettings(NamedTuple):
    #
    # URLs for top-level categories. These will appear in the sidebar.
    # URLs for item pages. These will not appear in the sidebar.
    URLS: List[URLConfig] = []
    #
    # Name of the admin data views section in admin panel
    NAME: str = "Admin Data Views"


SETTING_NAME = "ADMIN_DATA_VIEWS"

DEFAULTS: Dict[str, Any] = AdminDataViewsSettings()._asdict()

IMPORT_STRINGS: Set[Union[bytes, str]] = {"URLS"}

REMOVED_SETTINGS: Set[str] = set()


class SettingsHolder(holder.SettingsHolder):
    def perform_import(self, val: str, setting: str) -> Any:
        if setting in {"URLS"}:
            val: List[URLConfig]
            for i, item in enumerate(val):
                missing = {"route", "view", "name"}.difference(item.keys())
                if missing:
                    raise RuntimeError(f"Missing keys in ADMIN_DATA_VIEWS[{i}]: {missing}")

                item["route"] = item["route"].rstrip("/").lstrip("/")
                item["view"] = self.import_from_string(item["view"], setting)

                if item.get("items") is None:
                    item["items"] = None
                    continue

                missing = {"route", "view", "name"}.difference(item["items"].keys())
                if missing:
                    raise RuntimeError(f"Missing keys in ADMIN_DATA_VIEWS[{i}]['items']: {missing}")

                item["items"]["route"] = item["items"]["route"].rstrip("/").lstrip("/")
                item["items"]["view"] = self.import_from_string(item["items"]["view"], setting)

            return val

        return super().perform_import(val, setting)  # pragma: no cover


admin_data_settings = SettingsHolder(
    setting_name=SETTING_NAME,
    defaults=DEFAULTS,
    import_strings=IMPORT_STRINGS,
    removed_settings=REMOVED_SETTINGS,
)

reload_admin_data_settings = reload_settings(SETTING_NAME, admin_data_settings)
setting_changed.connect(reload_admin_data_settings)
