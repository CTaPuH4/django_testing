from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestsFixture(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Author')
        cls.reader = User.objects.create(username='Reader')
        cls.author_client = Client()
        cls.reader_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(
            title='Title',
            text='sometext',
            slug='some-slug',
            author=cls.author,
        )
        cls.home_url = reverse('notes:home')
        cls.list_url = reverse('notes:list')
        cls.add_url = reverse('notes:add')
        cls.success_url = reverse('notes:success')
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.note.slug,))
        cls.detail_url = reverse('notes:detail', args=(cls.note.slug,))
        cls.login_url = reverse('users:login')
        cls.logout_url = reverse('users:logout')
        cls.signup_url = reverse('users:signup')
