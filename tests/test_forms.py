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

 
