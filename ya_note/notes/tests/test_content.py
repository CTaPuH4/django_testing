from notes.forms import NoteForm
from notes.tests.fixtures import TestsFixture


class TestContent(TestsFixture):
    def test_note_list_availibility(self):
        for client, status in (
            (self.author_client, True),
            (self.reader_client, False)
        ):
            with self.subTest(client=client, status=status):
                response = client.get(self.list_url)
                self.assertTrue(
                    (self.note in response.context['object_list']) is status)

    def test_forms_availibility(self):
        for url in (self.edit_url, self.add_url):
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
