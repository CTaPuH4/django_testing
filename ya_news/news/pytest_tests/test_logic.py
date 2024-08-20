from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


def test_anonymous_user_cant_create_comment(client, news_id, form_data):
    client.post(reverse('news:detail', args=news_id), data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_can_create_comment(
        author, author_client, news, news_id, form_data):
    response = author_client.post(reverse('news:detail', args=news_id),
                                  data=form_data)
    assertRedirects(response,
                    str(reverse('news:detail', args=news_id)) + '#comments')
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text == form_data['text']
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(author_client, news_id):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(reverse(
        'news:detail', args=news_id), data=bad_words_data
    )
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_delete_comment(author_client, comment_id, news_id):
    url = reverse('news:delete', args=comment_id)
    response = author_client.delete(url)
    assertRedirects(response,
                    str(reverse('news:detail', args=news_id)) + '#comments'
                    )
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_cant_delete_comment_of_another_user(
        not_author_client, comment_id,):
    url = reverse('news:delete', args=comment_id)
    response = not_author_client.delete(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1


def test_author_can_edit_comment(
        author_client, comment, comment_id, news_id, form_data):
    url = reverse('news:edit', args=comment_id)
    response = author_client.post(url, data=form_data)
    assertRedirects(response,
                    str(reverse('news:detail', args=news_id)) + '#comments'
                    )
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment_from_db.text == form_data['text']


def test_user_cant_edit_comment_of_another_user(
        not_author_client, comment, comment_id, form_data):
    url = reverse('news:edit', args=comment_id)
    response = not_author_client.post(url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment_from_db.text == comment.text
