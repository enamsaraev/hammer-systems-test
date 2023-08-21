import pytest

from rest_framework.test import APIClient
from mixer.backend.django import mixer


@pytest.fixture()
def api():
    """Returns APIClient"""

    return APIClient()


@pytest.fixture
def api_login(db, api):
    user = mixer.blend('core.User')
    user.set_password('secretpass')
    user.save()
    api.login(phone=user.phone, password='secretpass')

    return api, user