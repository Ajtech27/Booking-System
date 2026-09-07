from app.models import User, Room, Booking
from app import db
from datetime import datetime, timedelta

def test_user_model(app, test_user):
    """Test User model."""
    assert test_user.username == 'testuser'
    assert test_user.email == 'test@example.com'
    assert test_user.role == 'user'
    assert test_user.bookings == []

def test_room_model(app, test_room):
    """Test Room model."""
    assert test_room.room_number == '101'
    assert test_room.room_type == 'Single'
    assert test_room.price_per_night == 100.0
    assert test_room.is_available == True
    assert test_room.capacity == 2

 

 
