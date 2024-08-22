from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'user, status, name',
    (
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK, 'edit_url'),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK, 'delete_url'),
        (pytest.lazy_fixture(
            'not_author_client'), HTTPStatus.OK, 'home_url'),
        (pytest.lazy_fixture(
            'not_author_client'), HTTPStatus.OK, 'detail_url'),
        (pytest.lazy_fixture(
            'not_author_client'), HTTPStatus.OK, 'login_url'),
        (pytest.lazy_fixture(
            'not_author_client'), HTTPStatus.OK, 'logout_url'),
        (pytest.lazy_fixture(
            'not_author_client'), HTTPStatus.OK, 'signup_url'),
        (pytest.lazy_fixture(
            'not_author_client'), HTTPStatus.NOT_FOUND, 'edit_url'),
        (pytest.lazy_fixture(
            'not_author_client'), HTTPStatus.NOT_FOUND, 'delete_url'),
    )
)
def test_pages_availability(user, status, name, all_urls):
    response = user.get(all_urls[name])
    assert response.status_code == status


@pytest.mark.parametrize(
    'name',
    ('edit_url', 'delete_url')
)
def test_redirect_for_anonymous_client(name, all_urls, client):
    login_url = all_urls['login_url']
    redirect_url = f'{login_url}?next={all_urls[name]}'
    response = client.get(all_urls[name])
    assertRedirects(response, redirect_url)
