from datetime import datetime, timedelta

from app.forms import RegistrationForm, LoginForm, BookingForm, RoomForm
from app.models import User

def test_registration_form_valid(app):
    """Test valid registration form."""
    form = RegistrationForm(
        username='newuser',
        email='new@example.com',
        password='password123',
        confirm_password='password123'
    )
    assert form.validate() == True

def test_registration_form_invalid_username(app, test_user):
    """Test registration with existing username."""
    form = RegistrationForm(
        username='testuser',  # Already exists
        email='another@example.com',
        password='password123',
        confirm_password='password123'
    )
    assert form.validate() == False
    assert 'Username already taken.' in form.username.errors

def test_registration_form_invalid_email(app, test_user):
    """Test registration with existing email."""
    form = RegistrationForm(
        username='anotheruser',
        email='test@example.com',  # Already exists
        password='password123',
        confirm_password='password123'
    )
    assert form.validate() == False
    assert 'Email already registered.' in form.email.errors

def test_registration_form_password_mismatch(app):
    """Test registration with mismatched passwords."""
    form = RegistrationForm(
        username='newuser',
        email='new@example.com',
        password='password123',
        confirm_password='different'
    )
    assert form.validate() == False
    assert 'Field must be equal to password' in str(form.confirm_password.errors)

def test_login_form_valid(app):
    """Test valid login form."""
    form = LoginForm(
        email='test@example.com',
        password='password123'
    )
    assert form.validate() == True

def test_booking_form_dates(app):
    """Test booking form with valid dates."""
    today = datetime.now().date()
    form = BookingForm(
        check_in=today + timedelta(days=1),
        check_out=today + timedelta(days=3)
    )
    assert form.validate() == True