import pytest
from django.urls import reverse
from django.contrib.messages import get_messages
from tables.models import FileUpload, Campaign


@pytest.mark.django_db
def test_successful_aggregation(client, django_user_model):
    django_user_model.objects.create_user(username='testuser', password='password123')
    client.login(username='testuser', password='password123')

    file_upload = FileUpload.objects.create()

    Campaign.objects.create(
        file_upload=file_upload,
        advertiser='Advertiser1',
        brand='Brand1',
        start_date='2024-01-01',
        end_date='2024-01-31',
        format='Format1',
        platform='Platform1',
        impressions=1000
    )

    url = reverse('aggregated_results', args=[file_upload.id])
    response = client.get(url)

    assert response.status_code == 200
    assert 'monthly_data' in response.context
    assert response.context['monthly_data'][0]['total_impressions'] == 1000


@pytest.mark.django_db
def test_file_not_found(client, django_user_model):
    django_user_model.objects.create_user(username='testuser', password='password123')
    client.login(username='testuser', password='password123')

    invalid_id = 9999
    url = reverse('aggregated_results', args=[invalid_id])
    response = client.get(url)

    messages = list(get_messages(response.wsgi_request))
    assert response.status_code == 302
    assert any('Завантаження не знайдено.' in m.message for m in messages)


@pytest.mark.django_db
def test_no_data_for_file(client, django_user_model):
    django_user_model.objects.create_user(username='testuser', password='password123')
    client.login(username='testuser', password='password123')

    file_upload = FileUpload.objects.create()

    url = reverse('aggregated_results', args=[file_upload.id])
    response = client.get(url)

    assert response.status_code == 200
    assert response.context['monthly_data'] == []


@pytest.mark.django_db
def test_template_rendering(client, django_user_model):
    django_user_model.objects.create_user(username='testuser', password='password123')
    client.login(username='testuser', password='password123')

    file_upload = FileUpload.objects.create()
    Campaign.objects.create(
        file_upload=file_upload,
        advertiser='Advertiser1',
        brand='Brand1',
        start_date='2024-01-01',
        end_date='2024-01-31',
        format='Format1',
        platform='Platform1',
        impressions=1000
    )

    url = reverse('aggregated_results', args=[file_upload.id])
    response = client.get(url)

    assert response.status_code == 200
    assert 'monthly_data' in response.context
    assert response.context['monthly_data'][0]['total_impressions'] == 1000
    assert response.context['top_15_platforms'][0]['platform_lower'] == 'platform1'
