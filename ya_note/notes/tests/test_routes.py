from http import HTTPStatus

from .fixtures import TestsFixture


class TestRoutes(TestsFixture):
    def test_anonymous_pages_availability(self):
        urls = (
            self.home_url,
            self.login_url,
            self.logout_url,
            self.signup_url,
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability(self):
        urls = (
            self.home_url,
            self.list_url,
            self.add_url,
            self.success_url,
            self.login_url,
            self.logout_url,
            self.signup_url,
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_edit_and_delete_availability(self):
        users_statuses = (
            (self.author_client, HTTPStatus.OK),
            (self.reader_client, HTTPStatus.NOT_FOUND),
        )
        for sub_client, status in users_statuses:
            for url in (self.edit_url, self.delete_url, self.detail_url):
                with self.subTest(sub_client=sub_client, url=url):
                    response = sub_client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_anonymous_client_redirect(self):
        urls = (
            self.list_url,
            self.add_url,
            self.success_url,
            self.edit_url,
            self.delete_url,
            self.detail_url,
        )
        for url in urls:
            with self.subTest(url=url):
                redirect_url = f'{self.login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
