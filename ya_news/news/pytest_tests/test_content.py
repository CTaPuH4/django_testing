from django.conf import settings

from news.forms import CommentForm


def test_news_count(client, bulk_news, all_urls):
    response = client.get(all_urls['home_url'])
    news_count = response.context['object_list'].count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, bulk_news, all_urls):
    response = client.get(all_urls['home_url'])
    all_dates = [news.date for news in response.context['object_list']]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(client, news, comments_bulk, all_urls):
    response = client.get(all_urls['detail_url'])
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


def test_anonymous_client_has_no_form(client, all_urls):
    response = client.get(all_urls['detail_url'])
    assert 'form' not in response.context


def test_authorized_client_has_form(author_client, all_urls):
    response = author_client.get(all_urls['detail_url'])
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
