from http import HTTPStatus

from pytils.translit import slugify

from .fixtures import TestsFixture
from notes.forms import WARNING
from notes.models import Note


class TestLogic(TestsFixture):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.form_data = {
            'title': 'TITLE',
            'text': 'TEXT',
            'slug': 'some-slug',
        }

    def test_anonymous_user_cant_create_note(self):
        notes_count_before = Note.objects.count()
        self.client.post(self.add_url, data=self.form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, notes_count_before)

    def test_user_can_create_note(self):
        Note.objects.all().delete()
        response = self.author_client.post(self.add_url, data=self.form_data)
        self.assertRedirects(response, self.success_url)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)
        note = Note.objects.get()
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.author, self.author)

    def test_same_slug_warning(self):
        self.author_client.post(self.add_url, data=self.form_data)
        notes_count_before = Note.objects.count()
        response = self.author_client.post(self.add_url, data=self.form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, notes_count_before)
        self.assertFormError(
            response,
            form='form',
            field='slug',
            errors=self.form_data['slug'] + WARNING
        )

    def test_slugify(self):
        Note.objects.all().delete()
        self.author_client.post(self.add_url, data={
            'title': self.form_data['title'],
            'text': self.form_data['text'],
        })
        note = Note.objects.get()
        slugified = slugify(self.form_data['title'])
        self.assertEqual(note.slug, slugified)

    def test_author_can_delete_note(self):
        notes_count_before = Note.objects.count()
        response = self.author_client.delete(self.delete_url)
        self.assertRedirects(response, self.success_url)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count_before - notes_count, 1)

    def test_user_cant_delete_note_of_another_user(self):
        notes_count_before = Note.objects.count()
        response = self.reader_client.delete(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, notes_count_before)

    def test_author_can_edit_note(self):
        response = self.author_client.post(self.edit_url, data=self.form_data)
        self.assertRedirects(response, self.success_url)
        new_note = Note.objects.get(slug=self.note.slug)
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.author, self.author)

    def test_user_cant_edit_note_of_another_user(self):
        response = self.reader_client.post(self.edit_url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        new_note = Note.objects.get(slug=self.note.slug)
        self.assertEqual(new_note.title, self.note.title)
        self.assertEqual(new_note.text, self.note.text)
        self.assertEqual(new_note.author, self.note.author)
