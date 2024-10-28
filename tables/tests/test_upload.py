import pytest
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from tables.models import FileUpload, Campaign


@pytest.mark.django_db
def test_successful_file_upload(client, django_user_model):
    django_user_model.objects.create_user(username='testuser', password='password123')
    client.login(username='testuser', password='password123')

    valid_file = SimpleUploadedFile(
        "valid.csv",
        b"Advertiser,Brand,Start,End,Format,Platform,Impr\n"
        b"Advertiser1,Brand1,2024-01-01,2024-01-31,Format1,Platform1,1000\n",
        content_type="text/csv"
    )

    url = reverse('file_upload')
    response = client.post(url, {'file': valid_file})

    assert response.status_code == 302
    assert FileUpload.objects.count() == 1
    assert Campaign.objects.count() == 1


@pytest.mark.django_db
def test_invalid_file_format(client, django_user_model):
    django_user_model.objects.create_user(username='testuser', password='password123')
    client.login(username='testuser', password='password123')

    invalid_file = SimpleUploadedFile(
        "invalid.txt",
        b"Some random text",
        content_type="text/plain"
    )

    url = reverse('file_upload')
    response = client.post(url, {'file': invalid_file})

    messages = list(get_messages(response.wsgi_request))
    assert response.status_code == 302
    assert "Непідтримуваний формат файлу." in [m.message for m in messages]
    assert FileUpload.objects.count() == 0


@pytest.mark.django_db
def test_missing_required_columns(client, django_user_model):
    django_user_model.objects.create_user(username='testuser', password='password123')
    client.login(username='testuser', password='password123')

    missing_columns_file = SimpleUploadedFile(
        "missing_columns.csv",
        b"Advertiser,Start,End,Platform,Impr\n"
        b"Advertiser1,2024-01-01,2024-01-31,Platform1,1000\n",
        content_type="text/csv"
    )

    url = reverse('file_upload')
    response = client.post(url, {'file': missing_columns_file})

    messages = list(get_messages(response.wsgi_request))
    assert response.status_code == 302
    assert "Некоректна структура файлу." in [m.message for m in messages]
    assert FileUpload.objects.count() == 0


@pytest.mark.django_db
def test_invalid_dates_in_file(client, django_user_model):
    django_user_model.objects.create_user(username='testuser', password='password123')
    client.login(username='testuser', password='password123')

    invalid_dates_file = SimpleUploadedFile(
        "invalid_dates.csv",
        b"Advertiser,Brand,Start,End,Format,Platform,Impr\n"
        b"Advertiser1,Brand1,invalid_date,2024-01-31,Format1,Platform1,1000\n",
        content_type="text/csv"
    )

    url = reverse('file_upload')
    response = client.post(url, {'file': invalid_dates_file})

    messages = list(get_messages(response.wsgi_request))
    assert response.status_code == 302
    assert "Невірний формат дати в рядку" in messages[0].message
    assert FileUpload.objects.count() == 1
    assert Campaign.objects.count() == 0


@pytest.mark.django_db
def test_file_with_missing_dates(client, django_user_model):
    django_user_model.objects.create_user(username='testuser', password='password123')
    client.login(username='testuser', password='password123')

    missing_dates_file = SimpleUploadedFile(
        "missing_dates.csv",
        b"Advertiser,Brand,Start,End,Format,Platform,Impr\n"
        b"Advertiser1,Brand1,,2024-01-31,Format1,Platform1,1000\n",
        content_type="text/csv"
    )

    url = reverse('file_upload')
    response = client.post(url, {'file': missing_dates_file})

    messages = list(get_messages(response.wsgi_request))
    assert response.status_code == 302
    assert "Некоректні або відсутні дані в колонках Start та/або End." in [m.message for m in messages]
    assert FileUpload.objects.count() == 0


@pytest.mark.django_db
def test_unexpected_error_handling(client, django_user_model, mocker):
    django_user_model.objects.create_user(username='testuser', password='password123')
    client.login(username='testuser', password='password123')

    mocker.patch('tables.views.pd.read_csv', side_effect=Exception("Test Exception"))

    valid_file = SimpleUploadedFile(
        "valid.csv",
        b"Advertiser,Brand,Start,End,Format,Platform,Impr\n"
        b"Advertiser1,Brand1,2024-01-01,2024-01-31,Format1,Platform1,1000\n",
        content_type="text/csv"
    )

    url = reverse('file_upload')
    response = client.post(url, {'file': valid_file})

    messages = list(get_messages(response.wsgi_request))
    assert response.status_code == 302
    assert any("Помилка при обробці файлу" in m.message for m in messages)
    assert FileUpload.objects.count() == 0
