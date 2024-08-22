from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news(db):
    news = News.objects.create(title='Заголовок', text='Текст')
    return news


@pytest.fixture
def bulk_news(db):
    today = datetime.today()
    News.objects.bulk_create(
        News(
            title=f'Новость {index}',
            text='sometext',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        news=news,
        text='Текст',
        author=author
    )
    return comment


@pytest.fixture
def comments_bulk(news, author):
    now = timezone.now()
    for index in range(10):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'text {index}'
        )
        comment.created = now + timedelta(days=index)
        comment.save()


@pytest.fixture
def all_urls(news, comment):
    all_urls = {
        'home_url': reverse('news:home'),
        'detail_url': reverse('news:detail', args=(news.id,)),
        'edit_url': reverse('news:edit', args=(comment.id,)),
        'delete_url': reverse('news:delete', args=(comment.id,)),
        'login_url': reverse('users:login'),
        'logout_url': reverse('users:logout'),
        'signup_url': reverse('users:signup'),
    }
    return all_urls
