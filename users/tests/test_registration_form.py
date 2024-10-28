import pytest
from django.contrib.auth import get_user_model
from users.forms import RegistrationForm

User = get_user_model()


@pytest.mark.django_db
def test_registration_form_valid():
    form_data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password1': 'strongpassword123',
        'password2': 'strongpassword123'
    }
    form = RegistrationForm(data=form_data)
    assert form.is_valid()
    user = form.save()
    assert user.username == form_data['username']
    assert user.email == form_data['email']
    assert user.check_password(form_data['password1'])


@pytest.mark.django_db
def test_registration_form_invalid_email():
    """
    Тест для реєстраційної форми з невалідним email.
    """
    form_data = {
        'username': 'testuser',
        'email': 'invalid-email',
        'password1': 'strongpassword123',
        'password2': 'strongpassword123'
    }
    form = RegistrationForm(data=form_data)
    assert not form.is_valid()
    assert 'email' in form.errors


@pytest.mark.django_db
def test_registration_form_password_mismatch():
    """
    Тест для форми з невідповідними паролями.
    """
    form_data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password1': 'strongpassword123',
        'password2': 'wrongpassword'
    }
    form = RegistrationForm(data=form_data)
    assert not form.is_valid()
    assert 'password2' in form.errors


@pytest.mark.django_db
def test_registration_form_existing_user():
    """
    Тест для реєстраційної форми з існуючим користувачем.
    """
    User.objects.create_user(username='testuser', email='testuser@example.com', password='password123')
    form_data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password1': 'strongpassword123',
        'password2': 'strongpassword123'
    }
    form = RegistrationForm(data=form_data)
    assert not form.is_valid()
    assert 'username' in form.errors
