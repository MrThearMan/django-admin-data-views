from __future__ import annotations

from collections.abc import Callable, ItemsView
from typing import Any, NamedTuple, TypedDict, Union

try:
    from typing import NotRequired
except ImportError:
    from typing_extensions import NotRequired

__all__ = [
    "Any",
    "AppDict",
    "AppModel",
    "Callable",
    "DictItems",
    "ItemContext",
    "ItemViewContext",
    "ItemsView",
    "NamedTuple",
    "NestedDict",
    "NotRequired",
    "SectionData",
    "TableContext",
    "TableViewContext",
    "URLConfig",
]


NestedDict = dict[str, Union[str, "NestedDict"]]
NestedItem = list[Union[str, NestedDict, "NestedItem"]]
DictItem = str | NestedDict | NestedItem
DictItems = tuple[DictItem, str]


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
    help_texts: NestedDict


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


class ItemViewContext(ItemContextLabeled, total=False):
    category_slug: str
    category_url: str
    download_button: bool


class ItemConfig(TypedDict):
    route: str
    view: str
    name: str


class URLConfig(TypedDict):
    route: str
    view: str
    name: str
    items: NotRequired[ItemConfig]
