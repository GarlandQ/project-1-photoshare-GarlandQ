import pytest

from django.contrib.auth.models import User


@pytest.mark.django_db
def test_create_user():
    User.objects.create_user(username='test', password='testPassword8')
    assert User.objects.count() == 1
