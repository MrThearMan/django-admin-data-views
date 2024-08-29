import re

import pytest

from admin_data_views.settings import admin_data_settings
from admin_data_views.templatetags.admin_data_utils import fields_with_help_texts
from admin_data_views.typing import SectionData
from admin_data_views.utils import render_with_item_view, render_with_table_view


def func(request):
    return {}


def test_missing_keys_in_admin_data_setting(settings):
    settings.ADMIN_DATA_VIEWS = {
        "URLS": [
            {
                "route": "foo/",
                "view": "example_project.project.urls.foo_list_view",
            },
        ],
    }

    with pytest.raises(RuntimeError, match=re.escape("Missing keys in ADMIN_DATA_VIEWS[0]: {'name'}")):
        admin_data_settings.URLS

    settings.ADMIN_DATA_VIEWS = {
        "URLS": [
            {
                "route": "foo/",
                "view": "example_project.project.urls.foo_list_view",
                "name": "foo_list",
                "items": {
                    "route": "<int:idd>/",
                    "view": "example_project.project.urls.foo_items_view",
                },
            },
        ],
    }

    with pytest.raises(
        RuntimeError,
        match=re.escape("Missing keys in ADMIN_DATA_VIEWS[0]['items']: {'name'}"),
    ):
        admin_data_settings.URLS


def test_missing_function_for_table_view_in_admin_data_setting(settings):
    settings.ADMIN_DATA_VIEWS = {
        "URLS": [
            {
                "route": "foo/",
                "view": "example_project.project.urls.foo_list_view",
                "name": "foo_list",
            },
        ],
    }

    with pytest.raises(
        ValueError,
        match="Cannot find 'tests.test_utils.func' in ADMIN_DATA_VIEWS setting.",
    ):
        render_with_table_view(func)(None)


def test_missing_function_for_item_view_in_from_admin_data_setting(settings):
    settings.ADMIN_DATA_VIEWS = {
        "URLS": [
            {
                "route": "foo/",
                "view": "example_project.project.urls.foo_list_view",
                "name": "foo_list",
            },
        ],
    }

    with pytest.raises(
        ValueError,
        match="Cannot find 'tests.test_utils.func' in ADMIN_DATA_VIEWS setting.",
    ):
        render_with_item_view(func)(None)


def test_fields_with_help_texts():
    section_data = SectionData(
        name=None,
        description=None,
        fields={"foo": "bar"},
        help_texts={"foo": "help"},
    )

    result = fields_with_help_texts(section_data)

    assert result == {
        "foo": ("bar", "help"),
    }


def test_fields_with_help_texts__nested():
    section_data = SectionData(
        name=None,
        description=None,
        fields={"foo": {"bar": "1"}},
        help_texts={"foo": {"bar": "help"}},
    )

    result = fields_with_help_texts(section_data)

    assert result == {
        "foo": ({"bar": ("1", "help")}, ""),
    }


def test_fields_with_help_texts__nested__main():
    section_data = SectionData(
        name=None,
        description=None,
        fields={"foo": {"bar": "1"}},
        help_texts={"foo": "help"},
    )

    result = fields_with_help_texts(section_data)

    assert result == {
        "foo": ({"bar": ("1", "")}, "help"),
    }


def test_fields_with_help_texts__nested__array():
    section_data = SectionData(
        name=None,
        description=None,
        fields={"foo": ["bar", "1"]},
        help_texts={"foo": "help"},
    )

    result = fields_with_help_texts(section_data)

    assert result == {
        "foo": (
            [
                ("bar", ""),
                ("1", ""),
            ],
            "help",
        ),
    }


def test_fields_with_help_texts__nested__array__dicts():
    section_data = SectionData(
        name=None,
        description=None,
        fields={"foo": [{"one": "bar"}, {"two": "1"}]},
        help_texts={"foo": "help"},
    )

    result = fields_with_help_texts(section_data)

    assert result == {
        "foo": (
            [
                (
                    {"one": ("bar", "")},
                    "",
                ),
                (
                    {"two": ("1", "")},
                    "",
                ),
            ],
            "help",
        ),
    }


def test_fields_with_help_texts__nested__array__dicts__sub():
    section_data = SectionData(
        name=None,
        description=None,
        fields={"foo": [{"one": "bar"}, {"two": "1"}]},
        help_texts={"foo": {"one": "this is one", "two": "this is two"}},
    )

    result = fields_with_help_texts(section_data)

    assert result == {
        "foo": (
            [
                (
                    {"one": ("bar", "this is one")},
                    "",
                ),
                (
                    {"two": ("1", "this is two")},
                    "",
                ),
            ],
            "",
        ),
    }
