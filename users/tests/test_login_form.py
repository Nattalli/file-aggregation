import pytest

from users.forms import LoginForm, RegistrationForm


@pytest.mark.django_db
def test_login_form_valid():
    form_data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password1': 'strongpassword123',
        'password2': 'strongpassword123'
    }
    RegistrationForm(data=form_data).save()

    form_data = {
        'username': 'testuser',
        'password': 'strongpassword123'
    }
    form = LoginForm(data=form_data)

    assert form.is_valid()


@pytest.mark.django_db
def test_login_form_missing_username():
    form_data = {
        'username': '',
        'password': 'password123'
    }
    form = LoginForm(data=form_data)

    assert not form.is_valid()
    assert 'username' in form.errors


@pytest.mark.django_db
def test_login_form_missing_password():
    form_data = {
        'username': 'testuser',
        'password': ''
    }
    form = LoginForm(data=form_data)

    assert not form.is_valid()
    assert 'password' in form.errors
