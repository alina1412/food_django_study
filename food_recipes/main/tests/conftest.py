import os

import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
from django.conf import settings

settings.SECRET_KEY = "test-secret-key"

django.setup()


@pytest.fixture(scope="session", autouse=True)
def django_db_setup(django_db_blocker):
    from django.core.management import call_command

    with django_db_blocker.unblock():
        call_command("makemigrations", verbosity=0)
        call_command("migrate", verbosity=0)
