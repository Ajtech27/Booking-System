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
 
