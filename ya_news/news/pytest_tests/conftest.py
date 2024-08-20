from datetime import datetime, timedelta

from django.conf import settings
from django.test.client import Client
from django.utils import timezone
import pytest

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
def news_id(news):
    return (news.pk,)


@pytest.fixture
def comment_id(comment):
    return (comment.pk,)


@pytest.fixture
def form_data():
    form_data = {'text': 'Текст комментария'}
    return form_data
