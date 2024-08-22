from http import HTTPStatus

from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

FORM_DATA = {'text': 'Текст комментария'}


def test_anonymous_user_cant_create_comment(client, all_urls):
    comments_count_before = Comment.objects.count()
    client.post(all_urls['detail_url'], data=FORM_DATA)
    comments_count = Comment.objects.count()
    assert comments_count == comments_count_before


def test_user_can_create_comment(author, author_client, news, all_urls):
    Comment.objects.all().delete()
    response = author_client.post(all_urls['detail_url'], data=FORM_DATA)
    assertRedirects(response, str(all_urls['detail_url']) + '#comments')
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text == FORM_DATA['text']
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(author_client, all_urls):
    comments_count_before = Comment.objects.count()
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(all_urls['detail_url'], data=bad_words_data)
    comments_count = Comment.objects.count()
    assert comments_count == comments_count_before
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING,
    )


def test_author_can_delete_comment(author_client, all_urls):
    comments_count_before = Comment.objects.count()
    response = author_client.delete(all_urls['delete_url'])
    assertRedirects(response, str(all_urls['detail_url']) + '#comments')
    comments_count = Comment.objects.count()
    assert comments_count_before - comments_count == 1


def test_user_cant_delete_comment_of_another_user(not_author_client, all_urls):
    comments_count_before = Comment.objects.count()
    response = not_author_client.delete(all_urls['delete_url'])
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == comments_count_before


def test_author_can_edit_comment(
        author_client, comment, all_urls):
    response = author_client.post(all_urls['edit_url'], data=FORM_DATA)
    assertRedirects(response, str(all_urls['detail_url']) + '#comments')
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment_from_db.text == FORM_DATA['text']
    assert comment_from_db.author == comment.author
    assert comment_from_db.news == comment.news


def test_user_cant_edit_comment_of_another_user(
        not_author_client, comment, all_urls):
    response = not_author_client.post(all_urls['edit_url'], data=FORM_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment_from_db.text == comment.text
    assert comment_from_db.author == comment.author
    assert comment_from_db.news == comment.news
