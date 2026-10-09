import pytest


@pytest.mark.django_db
@pytest.mark.parametrize("kind", ["json", "csv"])
def test_download__method_not_allowed(django_client, kind):
    result = django_client.get(f"/admin/admin-data-views/download/{kind}/")

    assert result.status_code == 405
    assert result.content == b"GET not supported."
    assert result["Allow"] == "POST"


@pytest.mark.django_db
@pytest.mark.parametrize("kind", ["json", "csv"])
def test_download__name_missing(django_client, kind):
    result = django_client.post(f"/admin/admin-data-views/download/{kind}/", data={"data": "[]"})

    assert result.status_code == 400
    assert result.content == b"'name' is required."


@pytest.mark.django_db
@pytest.mark.parametrize("kind", ["json", "csv"])
def test_download__data_missing(django_client, kind):
    result = django_client.post(f"/admin/admin-data-views/download/{kind}/", data={"name": "foo"})

    assert result.status_code == 400
    assert result.content == b"'data' is required."


@pytest.mark.django_db
def test_download_json(django_client):
    result = django_client.post("/admin/admin-data-views/download/json/", data={"name": "foo", "data": '{"a": [1]}'})

    assert result.status_code == 200
    assert result["Content-Type"] == "application/force-download"
    assert result["Content-Disposition"] == 'attachment; filename="foo.json"'
    assert result.content == b'{\n  "a": [\n    1\n  ]\n}'


@pytest.mark.django_db
def test_download_json__invalid_json(django_client):
    result = django_client.post("/admin/admin-data-views/download/json/", data={"name": "foo", "data": "{"})

    assert result.status_code == 400
    assert result.content == b"'data' is is not valid json."


@pytest.mark.django_db
def test_download_csv(django_client):
    result = django_client.post("/admin/admin-data-views/download/csv/", data={"name": "foo", "data": "a,b\n1,2"})

    assert result.status_code == 200
    assert result["Content-Type"] == "application/force-download"
    assert result["Content-Disposition"] == 'attachment; filename="foo.csv"'
    assert result.content == b"a,b\n1,2"
