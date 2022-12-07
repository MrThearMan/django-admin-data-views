from typing import Any, Callable, Dict, ItemsView, List, NamedTuple, Optional, Set, Tuple, TypedDict, Union


__all__ = [
    "Any",
    "AppDict",
    "AppModel",
    "Callable",
    "Dict",
    "DictItems",
    "ItemContext",
    "ItemsView",
    "ItemViewContext",
    "List",
    "NamedTuple",
    "NestedDict",
    "Optional",
    "SectionData",
    "Set",
    "TableContext",
    "TableViewContext",
    "Tuple",
    "Union",
    "URLConfig",
]


NestedDict = Dict[str, Union[str, "NestedDict"]]
NestedItem = List[Union[str, NestedDict, "NestedItem"]]
DictItem = Union[str, NestedDict, NestedItem]
DictItems = Tuple[DictItem, str]


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
    add_url: Optional[str]
    view_only: bool


class AppDict(TypedDict):
    name: str
    app_label: str
    app_url: str
    has_module_perms: bool
    models: List[AppModel]


class TableContextBase(TypedDict):
    title: str
    table: Dict[str, List[Any]]


class TableContext(TableContextBase, total=False):
    subtitle: str
    extra_context: Dict[str, Any]


class TableViewContext(TypedDict):
    slug: str
    title: str
    subtitle: Optional[str]
    app_label: str
    headers: List[str]
    rows: List[List[Any]]


class SectionDataBase(TypedDict):
    name: Optional[str]
    description: Optional[str]
    fields: NestedDict


class SectionData(SectionDataBase, total=False):
    help_texts: NestedDict


class ItemContextBase(TypedDict):
    slug: Any
    title: str
    data: List[SectionData]


class ItemContext(ItemContextBase, total=False):
    image: str
    subtitle: str
    extra_context: Dict[str, Any]


class ItemContextLabeled(ItemContext):
    app_label: str


class ItemViewContext(ItemContextLabeled, total=False):
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
    items: Optional[ItemConfig]
