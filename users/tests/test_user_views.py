import pytest
import uuid

from django.urls import reverse
from django.contrib.auth.models import User


class TestLogin():
    def test_login_get(self, client):
        response = client.get(reverse('login'))
        assert response.status_code == 200


    def test_login_post(self, client, create_user, test_password):
        user = create_user()
        response = client.post(reverse('login'), {'username': user.username, 'password': test_password}, follow=True)

        assert response.status_code == 200
        assert response.wsgi_request.user == user
        assert response.wsgi_request.user.is_authenticated
        assert response.redirect_chain[0][0] == reverse('index')


    def test_login_post_wrong_password(self, client, create_user):
        user = create_user()
        response = client.post(reverse('login'), {'username': user.username, 'password': 'wrongPassword'})

        assert response.status_code == 200
        assert not response.wsgi_request.user.is_authenticated


class TestSignUp():
    def test_signup_get(self, client):
        response = client.get(reverse('signup'))
        assert response.status_code == 200


    @pytest.mark.django_db(transaction=True)
    def test_signup_post(self, client, django_user_model, test_password):
        username = str(uuid.uuid4())
        data = {'username': username, 'password1': test_password, 'password2': test_password}
        response = client.post(reverse('signup'), data, follow=True)

        assert response.status_code == 200
        assert response.wsgi_request.user.is_authenticated
        assert response.redirect_chain[0][0] == reverse('index')

        created_user = django_user_model.objects.get(username=username)
        assert created_user


    @pytest.mark.django_db(transaction=True)
    def test_signup_post_invalid_form(self, client, django_user_model):
        username = str(uuid.uuid4())
        data = {'username': username, 'password1': 'weak', 'password2': 'mismatch'}
        response = client.post(reverse('signup'), data)

        assert response.status_code == 200
        assert not response.wsgi_request.user.is_authenticated

        with pytest.raises(User.DoesNotExist):
            django_user_model.objects.get(username=username)


@pytest.mark.parametrize('route_name', ['login', 'signup'])
def test_redirect_to_index_for_logged_in_users(auto_login_user, route_name):
    client, _ = auto_login_user()
    response = client.get(reverse(route_name), follow=True)

    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse('index')


def test_logout(auto_login_user):
    client, _ = auto_login_user()
    response = client.get(reverse('logout'), follow=True)

    assert response.status_code == 200
    assert not response.wsgi_request.user.is_authenticated
