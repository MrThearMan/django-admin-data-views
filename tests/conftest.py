import pytest
from django.contrib.auth.models import User
from django.test import Client


@pytest.fixture(scope="session")
def superuser(django_db_setup, django_db_blocker) -> User:
    with django_db_blocker.unblock():
        user: User = User.objects.get_or_create(
            username="x",
            email="user@user.com",
            is_staff=True,
            is_superuser=True,
        )[0]
        user.set_password("x")
        user.save()

    return user


@pytest.fixture(scope="session")
def django_client(django_db_blocker, superuser: User) -> Client:
    client = Client()
    with django_db_blocker.unblock():
        client.force_login(superuser)
    return client
