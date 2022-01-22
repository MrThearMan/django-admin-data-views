import pytest
from bs4 import BeautifulSoup
from django.http import HttpResponse


@pytest.mark.django_db
def test_admin_main_page(django_client):
    result: HttpResponse = django_client.get("/admin/", follow=True)
    soup = BeautifulSoup(result.content, features="html.parser")

    main_content = soup.find(name="div", attrs={"id": "content-main"})
    admin_data_views = main_content.find(name="div", attrs={"class": "app-admin-data-views"})

    assert admin_data_views is not None

    title_link = admin_data_views.find(name="caption").find(name="a")

    assert title_link.get("href") == "/admin/admin-data-views/"
    assert title_link.text == "Admin Data Views"

    foo_list = admin_data_views.find(name="tr", attrs={"class": "model-foo_list"}).find("th").find("a")
    bar_list = admin_data_views.find(name="tr", attrs={"class": "model-bar_list"}).find("th").find("a")
    fizz_item = admin_data_views.find(name="tr", attrs={"class": "model-fizz"}).find("th").find("a")
    buzz_item = admin_data_views.find(name="tr", attrs={"class": "model-buzz"}).find("th").find("a")

    assert foo_list.text == "Foo List"
    assert foo_list.get("href") == "/admin/admin-data-views/foo/"

    assert bar_list.text == "Bar List"
    assert bar_list.get("href") == "/admin/admin-data-views/bar/"

    assert fizz_item.text == "Fizz"
    assert fizz_item.get("href") == "/admin/admin-data-views/fizz/"

    assert buzz_item.text == "Buzz"
    assert buzz_item.get("href") == "/admin/admin-data-views/buzz/"


@pytest.mark.django_db
def test_admin_data_views_list(django_client):
    result: HttpResponse = django_client.get("/admin/admin-data-views/", follow=True)
    soup = BeautifulSoup(result.content, features="html.parser")

    main_content = soup.find(name="div", attrs={"id": "content-main"})
    admin_data_views = main_content.find(name="div", attrs={"class": "app-admin-data-views"})

    assert admin_data_views is not None

    title_link = admin_data_views.find(name="caption").find(name="a")

    assert title_link.get("href") == "/admin/admin-data-views/"
    assert title_link.text == "Admin Data Views"

    foo_list = admin_data_views.find(name="tr", attrs={"class": "model-foo_list"}).find("th").find("a")
    bar_list = admin_data_views.find(name="tr", attrs={"class": "model-bar_list"}).find("th").find("a")
    fizz_item = admin_data_views.find(name="tr", attrs={"class": "model-fizz"}).find("th").find("a")
    buzz_item = admin_data_views.find(name="tr", attrs={"class": "model-buzz"}).find("th").find("a")

    assert foo_list.text == "Foo List"
    assert foo_list.get("href") == "/admin/admin-data-views/foo/"

    assert bar_list.text == "Bar List"
    assert bar_list.get("href") == "/admin/admin-data-views/bar/"

    assert fizz_item.text == "Fizz"
    assert fizz_item.get("href") == "/admin/admin-data-views/fizz/"

    assert buzz_item.text == "Buzz"
    assert buzz_item.get("href") == "/admin/admin-data-views/buzz/"


@pytest.mark.django_db
def test_admin_foo_list_view(django_client):
    result: HttpResponse = django_client.get("/admin/admin-data-views/foo/", follow=True)
    soup = BeautifulSoup(result.content, features="html.parser")

    content = soup.find(name="div", attrs={"id": "content"})

    assert content.find(name="h1").text == "Foo items"

    list_table = content.find(name="form", attrs={"id": "changelist-form"})
    headers = list_table.find("table").find(name="thead").findAll(name="th")

    assert len(headers) == 2

    assert headers[0].find(name="span").text == "Name"
    assert headers[1].find(name="span").text == "Value"

    rows = list_table.find("table").find(name="tbody").findAll(name="tr")

    assert len(rows) == 2

    row_1_items = rows[0].findAll(name="td")

    assert len(row_1_items) == 2

    row_1_link = row_1_items[0].find(name="a")

    assert row_1_link.get("href") == "/admin/admin-data-views/foo/123/"
    assert row_1_link.text == "Foo"
    assert row_1_items[1].text == "1"

    row_2_items = rows[1].findAll(name="td")

    assert len(row_2_items) == 2

    row_2_link = row_2_items[0].find(name="a")

    assert row_2_link.get("href") == "/admin/admin-data-views/foo/124/"
    assert row_2_link.text == "Bar"
    assert row_2_items[1].text == "2"


@pytest.mark.django_db
def test_admin_foo_item_view(django_client):
    result: HttpResponse = django_client.get("/admin/admin-data-views/foo/123/", follow=True)
    soup = BeautifulSoup(result.content, features="html.parser")

    content = soup.find(name="div", attrs={"id": "content"})

    assert content.find(name="h1").text == "This is 123"

    sections = content.findAll(name="fieldset")

    assert len(sections) == 2
    section_1_title = sections[0].find(name="h2")
    section_1_subtitle = sections[0].find(name="div", attrs={"class": "description"})
    section_1_fields = sections[0].findAll(name="div", attrs={"class": "fieldBox"})

    assert section_1_title is None
    assert section_1_subtitle is None
    assert len(section_1_fields) == 1

    section_1_label_1 = section_1_fields[0].find(name="label")
    section_1_input_1 = section_1_fields[0].find(name="input")

    assert section_1_label_1.text == "Foo"
    assert section_1_input_1.get("value") == "123"

    section_2_title = sections[1].find(name="h2")
    section_2_subtitle = sections[1].find(name="div", attrs={"class": "description"})
    section_2_fields = sections[1].findAll(name="div", attrs={"class": "fieldBox"})

    assert section_2_title.text == "This is another section"
    assert section_2_subtitle.text == "This is the description for this section"
    assert len(section_2_fields) == 1

    section_2_label_1 = section_2_fields[0].find(name="label")
    section_2_input_1 = section_2_fields[0].find(name="input")

    assert section_2_label_1.text == "Fizz"
    assert section_2_input_1.get("value") == "246"


@pytest.mark.django_db
def test_admin_bar_list_view(django_client):
    result: HttpResponse = django_client.get("/admin/admin-data-views/bar/", follow=True)
    soup = BeautifulSoup(result.content, features="html.parser")

    content = soup.find(name="div", attrs={"id": "content"})

    assert content.find(name="h1").text == "Bar items"

    list_table = content.find(name="form", attrs={"id": "changelist-form"})
    headers = list_table.find("table").find(name="thead").findAll(name="th")

    assert len(headers) == 2

    assert headers[0].find(name="span").text == "Fizz"
    assert headers[1].find(name="span").text == "Buzz"

    rows = list_table.find("table").find(name="tbody").findAll(name="tr")

    assert len(rows) == 2

    row_1_items = rows[0].findAll(name="td")

    assert len(row_1_items) == 2

    row_1_link = row_1_items[0].find(name="a")

    assert row_1_link.get("href") == "/admin/admin-data-views/bar/bar/"
    assert row_1_link.text == "X"
    assert row_1_items[1].text == "1"

    row_2_items = rows[1].findAll(name="td")

    assert len(row_2_items) == 2

    row_2_link = row_2_items[0].find(name="a")

    assert row_2_link.get("href") == "/admin/admin-data-views/bar/bar/"
    assert row_2_link.text == "Y"
    assert row_2_items[1].text == "2"


@pytest.mark.django_db
def test_admin_bar_item_view(django_client):
    result: HttpResponse = django_client.get("/admin/admin-data-views/bar/bar/", follow=True)
    soup = BeautifulSoup(result.content, features="html.parser")

    content = soup.find(name="div", attrs={"id": "content"})

    assert content.find(name="h1").text == "Bar page"

    sections = content.findAll(name="fieldset")

    assert len(sections) == 2
    section_1_title = sections[0].find(name="h2")
    section_1_subtitle = sections[0].find(name="div", attrs={"class": "description"})
    section_1_fields = sections[0].findAll(name="div", attrs={"class": "fieldBox"})

    assert section_1_title is None
    assert section_1_subtitle is None
    assert len(section_1_fields) == 1

    section_1_label_1 = section_1_fields[0].find(name="label")
    section_1_input_1 = section_1_fields[0].find(name="input")

    assert section_1_label_1.text == "Foo"
    assert section_1_input_1.get("value") == "Bar"

    section_2_title = sections[1].find(name="h2")
    section_2_subtitle = sections[1].find(name="div", attrs={"class": "description"})
    section_2_fields = sections[1].findAll(name="div", attrs={"class": "fieldBox"})

    assert section_2_title.text == "This is another section"
    assert section_2_subtitle.text == "This is the description for this section"
    assert len(section_2_fields) == 1

    section_2_label_1 = section_2_fields[0].find(name="label")
    section_2_input_1 = section_2_fields[0].find(name="input")

    assert section_2_label_1.text == "Fizz"
    assert section_2_input_1.get("value") == "Buzz"


@pytest.mark.django_db
def test_admin_fizz_list_view(django_client):
    result: HttpResponse = django_client.get("/admin/admin-data-views/fizz/", follow=True)
    soup = BeautifulSoup(result.content, features="html.parser")

    content = soup.find(name="div", attrs={"id": "content"})

    assert content.find(name="h1").text == "Fizz view"

    list_table = content.find(name="form", attrs={"id": "changelist-form"})
    headers = list_table.find("table").find(name="thead").findAll(name="th")

    assert len(headers) == 2

    assert headers[0].find(name="span").text == "A"
    assert headers[1].find(name="span").text == "B"

    rows = list_table.find("table").find(name="tbody").findAll(name="tr")

    assert len(rows) == 2

    row_1_items = rows[0].findAll(name="td")

    assert len(row_1_items) == 2

    assert row_1_items[0].text == "X"
    assert row_1_items[1].text == "1"

    row_2_items = rows[1].findAll(name="td")

    assert len(row_2_items) == 2

    assert row_2_items[0].text == "Y"
    assert row_2_items[1].text == "2"


@pytest.mark.django_db
def test_admin_buzz_item_view(django_client):
    result: HttpResponse = django_client.get("/admin/admin-data-views/buzz", follow=True)
    soup = BeautifulSoup(result.content, features="html.parser")

    content = soup.find(name="div", attrs={"id": "content"})

    assert content.find(name="h1").text == "Buzz page"

    sections = content.findAll(name="fieldset")

    assert len(sections) == 1
    section_1_title = sections[0].find(name="h2")
    section_1_subtitle = sections[0].find(name="div", attrs={"class": "description"})
    section_1_fields = sections[0].findAll(name="div", attrs={"class": "fieldBox"})

    assert section_1_title is None
    assert section_1_subtitle is None
    assert len(section_1_fields) == 1

    section_1_label_1 = section_1_fields[0].find(name="label")
    section_1_input_1 = section_1_fields[0].find(name="input")

    assert section_1_label_1.text == "Foo"
    assert section_1_input_1.get("value") == "Bar"
