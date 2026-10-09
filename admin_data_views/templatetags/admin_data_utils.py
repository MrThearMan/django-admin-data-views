from __future__ import annotations

import json
import re
from typing import TYPE_CHECKING

from django import template

if TYPE_CHECKING:
    from admin_data_views.typing import (
        Any,
        FormattedField,
        FormattedFields,
        HelpTexts,
        ItemsView,
        NestedDict,
        NestedValue,
        SectionData,
    )

register = template.Library()

LINK_TEMPLATE = re.compile(r'<a href=".*">(?P<value>.*)</a>')


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
def to_csv(value: list[list[str]]) -> str:
    """Convert to csv string"""
    string = ""
    for row in value:
        row_string = ""
        for item in row:
            match = LINK_TEMPLATE.match(item)
            if match is not None:
                item = match.group("value")  # noqa: PLW2901
            row_string += f"{item},"

        string += row_string[:-1] + "\n"

    return string[:-1]


@register.filter
def fields_with_help_texts(section_data: SectionData) -> FormattedFields:
    """Add help texts and iterate as dict items."""

    def add_help_text(fields: NestedDict, help_texts: HelpTexts) -> FormattedFields:
        formatted_fields: FormattedFields = {}

        for key, value in fields.items():
            help_text = help_texts.get(key, "")

            if isinstance(value, dict):
                if isinstance(help_text, str):
                    formatted_fields[key] = (add_help_text(value, {}), help_text)
                else:
                    formatted_fields[key] = (add_help_text(value, help_text), "")
            elif isinstance(value, list):
                values = add_help_text_to_list(value, {} if isinstance(help_text, str) else help_text)
                formatted_fields[key] = (values, help_text if isinstance(help_text, str) else "")
            else:
                formatted_fields[key] = (value, help_text)

        return formatted_fields

    def add_help_text_to_list(items: list[NestedValue], help_texts: HelpTexts) -> list[FormattedField]:
        values: list[FormattedField] = []
        for item in items:
            if isinstance(item, dict):
                values.append((add_help_text(item, help_texts), ""))
            elif isinstance(item, list):
                values.append((add_help_text_to_list(item, help_texts), ""))
            else:
                values.append((item, ""))

        return values

    return add_help_text(section_data["fields"], section_data.get("help_texts", {}))
