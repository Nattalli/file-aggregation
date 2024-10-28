import pytest
from users.models import LogEntry
from users.utils import log_to_model


@pytest.mark.django_db
def test_log_to_model_without_user():
    log_to_model(level='INFO', message='Test message without user')

    assert LogEntry.objects.count() == 1

    log_entry = LogEntry.objects.first()

    assert log_entry.level == 'INFO'
    assert log_entry.message == 'Test message without user'
    assert log_entry.user is None


@pytest.mark.django_db
def test_log_to_model_with_user(django_user_model):
    user = django_user_model.objects.create_user(username='testuser', password='password123')

    log_to_model(level='ERROR', message='Test message with user', user=user)

    assert LogEntry.objects.count() == 1

    log_entry = LogEntry.objects.first()

    assert log_entry.level == 'ERROR'
    assert log_entry.message == 'Test message with user'
    assert log_entry.user == user


@pytest.mark.django_db
def test_log_to_model_multiple_entries(django_user_model):
    user = django_user_model.objects.create_user(username='testuser', password='password123')

    log_to_model(level='INFO', message='First message')
    log_to_model(level='WARNING', message='Second message', user=user)
    log_to_model(level='ERROR', message='Third message')

    assert LogEntry.objects.count() == 3

    first_log, second_log, third_log = LogEntry.objects.all()

    assert first_log.level == 'INFO'
    assert first_log.message == 'First message'
    assert first_log.user is None

    assert second_log.level == 'WARNING'
    assert second_log.message == 'Second message'
    assert second_log.user == user

    assert third_log.level == 'ERROR'
    assert third_log.message == 'Third message'
    assert third_log.user is None
