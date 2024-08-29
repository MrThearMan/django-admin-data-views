from __future__ import annotations

import json
from typing import TYPE_CHECKING

from django import template

if TYPE_CHECKING:
    from admin_data_views.typing import Any, DictItems, ItemsView, NestedDict, SectionData

register = template.Library()


@register.filter
def get_type(value: Any) -> str:
    """Get item type as a string."""
    return type(value).__name__


@register.filter
def items(value: dict[str, Any]) -> ItemsView[str, Any]:
    """Get dict items."""
    return value.items()


@register.filter
def jsonify(value: dict[str, Any] | list[Any]) -> str:
    """Convert to json string"""
    return json.dumps(value, default=str)


@register.filter
def fields_with_help_texts(section_data: SectionData) -> dict[str, DictItems]:
    """Add help texts and iterate as dict items."""

    def add_help_text(fields: NestedDict, help_texts: NestedDict) -> dict[str, DictItems]:
        formatted_fields: dict[str, DictItems] = {}

        for key, value in fields.items():
            help_text: str | NestedDict = help_texts.get(key, "")

            if isinstance(value, dict):
                if isinstance(help_text, str):
                    formatted_fields[key] = (add_help_text(value, {}), help_text)
                else:
                    formatted_fields[key] = (add_help_text(value, help_text), "")
            elif isinstance(value, list):
                values = []
                for item in value:
                    if not isinstance(item, (dict, list)):
                        values.append((item, ""))
                    else:
                        res = add_help_text(item, {} if isinstance(help_text, str) else help_text)
                        if not isinstance(res, tuple):
                            res = (res, "")
                        values.append(res)

                formatted_fields[key] = (values, help_text if isinstance(help_text, str) else "")
            else:
                formatted_fields[key] = (value, help_text)

        return formatted_fields

    return add_help_text(section_data["fields"], section_data.get("help_texts", {}))
