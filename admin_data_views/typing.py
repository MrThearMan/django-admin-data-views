from typing import Any, Dict, List, Optional, TypedDict


__all__ = [
    "AppDict",
    "AppModel",
    "TableContext",
    "ItemContext",
    "URLConfig",
]


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


class TableContext(TypedDict):
    title: str
    subtitle: Optional[str]
    table: Dict[str, List[Any]]


class SectionData(TypedDict):
    name: Optional[str]
    description: Optional[str]
    fields: Dict[str, Any]


class ItemContext(TypedDict):
    slug: Any
    title: str
    subtitle: Optional[str]
    image: Optional[str]
    data: List[SectionData]


class ItemConfig(TypedDict):
    route: str
    view: str
    name: str


class URLConfig(TypedDict):
    route: str
    view: str
    name: str
    items: Optional[ItemConfig]
