import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.messages import get_messages
from users.forms import LoginForm

User = get_user_model()


@pytest.mark.django_db
def test_register_view(client):
    url = reverse('register')
    form_data = {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password1': 'testpassword123',
        'password2': 'testpassword123'
    }
    response = client.post(url, form_data)

    assert response.status_code == 302
    assert response.url == reverse('login')

    user_exists = User.objects.filter(username='newuser').exists()
    assert user_exists

    messages = list(get_messages(response.wsgi_request))
    assert "Реєстрація успішна. Ви можете увійти в систему." in [m.message for m in messages]


@pytest.mark.django_db
def test_register_view_invalid_data(client):
    url = reverse('register')
    form_data = {
        'username': 'newuser',
        'email': 'invalid-email',
        'password1': 'testpassword123',
        'password2': 'testpassword123'
    }
    response = client.post(url, form_data)

    user_exists = User.objects.filter(username='newuser').exists()
    assert not user_exists

    form = response.context['form']
    assert not form.is_valid()
    assert 'email' in form.errors


@pytest.mark.django_db
def test_login_view_success(client, django_user_model):
    django_user_model.objects.create_user(username='testuser', password='password123')
    url = reverse('login')
    form_data = {
        'username': 'testuser',
        'password': 'password123'
    }
    response = client.post(url, form_data)

    assert response.status_code == 302
    assert response.url == reverse('file_upload')

    messages = list(get_messages(response.wsgi_request))
    assert "Вхід виконано успішно." in [m.message for m in messages]


@pytest.mark.django_db
def test_login_view_invalid_credentials(client):
    url = reverse('login')
    form_data = {
        'username': 'wronguser',
        'password': 'wrongpassword'
    }
    response = client.post(url, form_data)

    messages = list(get_messages(response.wsgi_request))
    assert "Неправильні ім'я користувача або пароль." in [m.message for m in messages]

    form = response.context['form']
    assert isinstance(form, LoginForm)
    assert not form.is_valid()


@pytest.mark.django_db
def test_logout_view(client, django_user_model):
    django_user_model.objects.create_user(username='testuser', password='password123')
    client.login(username='testuser', password='password123')

    url = reverse('logout')
    response = client.get(url)

    assert response.status_code == 302
    assert response.url == reverse('login')

    messages = list(get_messages(response.wsgi_request))
    assert "Ви вийшли з акаунту." in [m.message for m in messages]
