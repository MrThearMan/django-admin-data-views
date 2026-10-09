from __future__ import annotations

from collections.abc import Callable, ItemsView
from typing import Any, NamedTuple, NotRequired, TypedDict, Union

__all__ = [
    "Any",
    "AppDict",
    "AppModel",
    "Callable",
    "DictItems",
    "FormattedField",
    "FormattedFields",
    "HelpTexts",
    "ItemContext",
    "ItemViewContext",
    "ItemsView",
    "NamedTuple",
    "NestedDict",
    "NestedValue",
    "NotRequired",
    "SectionData",
    "TableContext",
    "TableViewContext",
    "URLConfig",
]


NestedValue = Union[str, int, float, bool, None, "NestedDict", list["NestedValue"]]
NestedDict = dict[str, NestedValue]
HelpTexts = dict[str, Union[str, "HelpTexts"]]
NestedItem = list[Union[str, NestedDict, "NestedItem"]]
DictItem = str | NestedDict | NestedItem
DictItems = tuple[DictItem, str]

# Fields paired with their help texts, as rendered by the item view templates.
FormattedFields = dict[str, "FormattedField"]
FormattedField = tuple[NestedValue | FormattedFields | list["FormattedField"], str]


class Perms(TypedDict):
    add: bool
    change: bool
    delete: bool
    view: bool


class AppModel(TypedDict):
    name: str
    object_name: str
    perms: Perms
    admin_url: str
    add_url: str | None
    view_only: bool


class AppDict(TypedDict):
    name: str
    app_label: str
    app_url: str
    has_module_perms: bool
    models: list[AppModel]


class TableContextBase(TypedDict):
    title: str
    table: dict[str, list[Any]]


class TableContext(TableContextBase, total=False):
    subtitle: str
    download_button: bool
    extra_context: dict[str, Any]


class TableViewContext(TypedDict):
    slug: str
    title: str
    subtitle: str | None
    download_button: bool
    app_label: str
    headers: list[str]
    rows: list[list[Any]]


class SectionDataBase(TypedDict):
    name: str | None
    description: str | None
    fields: NestedDict


class SectionData(SectionDataBase, total=False):
    help_texts: HelpTexts


class ItemContextBase(TypedDict):
    slug: Any
    title: str
    data: list[SectionData]


class ItemContext(ItemContextBase, total=False):
    image: str
    subtitle: str
    download_button: bool
    extra_context: dict[str, Any]


class ItemContextLabeled(ItemContext):
    app_label: str


class ItemViewContextBase(TypedDict):
    slug: Any
    title: str
    data: list[SectionData]
    app_label: str


class ItemViewContext(ItemViewContextBase, total=False):
    image: str | None
    subtitle: str | None
    download_button: bool
    extra_context: dict[str, Any]
    category_slug: str
    category_url: str


class ItemConfig(TypedDict):
    route: str
    view: str
    name: str


class URLConfig(TypedDict):
    route: str
    view: str
    name: str
    items: NotRequired[ItemConfig]
