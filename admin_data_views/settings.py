from typing import Any, Dict, List, NamedTuple, Optional, Set, Union

from django.conf import settings
from django.test.signals import setting_changed
from settings_holder import holder

from .typing import URLConfig


__all__ = [
    "admin_data_settings",
]


class AdminDataViewsSettings(NamedTuple):
    #
    # URLs for top-level cateories. These will appear in the sidebar.
    # URLs for item pages. These will not appear in the sidebar.
    URLS: List[URLConfig] = []


USER_SETTINGS: Optional[Dict[str, Any]] = getattr(settings, "ADMIN_DATA_VIEWS", None)

DEFAULTS: Dict[str, Any] = AdminDataViewsSettings()._asdict()

IMPORT_STRINGS: Set[Union[bytes, str]] = {"URLS"}

REMOVED_SETTINGS: Set[str] = set()


class SettingsHolder(holder.SettingsHolder):
    def perform_import(self, val: str, setting: str) -> Any:
        if setting in {"URLS"}:
            val: List[URLConfig]
            for item in val:
                missing = {"route", "view", "name"}.difference(item.keys())
                if missing:
                    raise RuntimeError(f"Missing keys in ADMIN_DATA_VIEWS: {missing}")

                item["route"] = item["route"].rstrip("/").lstrip("/")
                item["view"] = self.import_from_string(item["view"], setting)  # type: ignore

                if item.get("items") is None:
                    item["items"] = None
                    continue

                missing = {"route", "view", "name"}.difference(item["items"].keys())
                if missing:
                    raise RuntimeError(f"Missing keys in ADMIN_DATA_VIEWS['items']: {missing}")

                item["items"]["route"] = item["items"]["route"].rstrip("/").lstrip("/")
                item["items"]["view"] = self.import_from_string(item["items"]["view"], setting)  # type: ignore

            return val

        return super().perform_import(val, setting)


admin_data_settings = SettingsHolder(
    user_settings=USER_SETTINGS,
    defaults=DEFAULTS,
    import_strings=IMPORT_STRINGS,
    removed_settings=REMOVED_SETTINGS,
)


def reload_settings(*args, **kwargs) -> None:  # pylint: disable=W0613
    setting, value = kwargs["setting"], kwargs["value"]

    if setting == "ADMIN_DATA_VIEWS":
        admin_data_settings.reload(new_user_settings=value)


setting_changed.connect(reload_settings)
