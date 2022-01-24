import re

import pytest

from admin_data_views.settings import admin_data_settings
from admin_data_views.utils import render_with_item_view, render_with_table_view


def func(request):
    return {}


def test_missing_keys_in_admin_data_setting(settings):
    settings.ADMIN_DATA_VIEWS = {
        "URLS": [
            {
                "route": "foo/",
                "view": "tests.django.urls.foo_list_view",
            },
        ],
    }

    with pytest.raises(RuntimeError, match=re.escape("Missing keys in ADMIN_DATA_VIEWS[0]: {'name'}")):
        urls = admin_data_settings.URLS

    settings.ADMIN_DATA_VIEWS = {
        "URLS": [
            {
                "route": "foo/",
                "view": "tests.django.urls.foo_list_view",
                "name": "foo_list",
                "items": {
                    "route": "<int:idd>/",
                    "view": "tests.django.urls.foo_items_view",
                },
            },
        ],
    }

    with pytest.raises(RuntimeError, match=re.escape("Missing keys in ADMIN_DATA_VIEWS[0]['items']: {'name'}")):
        urls = admin_data_settings.URLS


def test_missing_function_for_table_view_in_admin_data_setting(settings):
    settings.ADMIN_DATA_VIEWS = {
        "URLS": [
            {
                "route": "foo/",
                "view": "tests.django.urls.foo_list_view",
                "name": "foo_list",
            },
        ],
    }

    with pytest.raises(ValueError, match="Cannot find 'tests.test_utils.func' in ADMIN_DATA_VIEWS setting."):
        render_with_table_view(func)(None)  # noqa


def test_missing_function_for_item_view_in_from_admin_data_setting(settings):
    settings.ADMIN_DATA_VIEWS = {
        "URLS": [
            {
                "route": "foo/",
                "view": "tests.django.urls.foo_list_view",
                "name": "foo_list",
            },
        ],
    }

    with pytest.raises(ValueError, match="Cannot find 'tests.test_utils.func' in ADMIN_DATA_VIEWS setting."):
        render_with_item_view(func)(None)  # noqa
