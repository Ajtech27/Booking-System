from app.models import User, Room, Booking
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

def test_booking_creation(app, test_user, test_room):
    """Test Booking creation."""
    today = datetime.now().date()
    check_in = today + timedelta(days=1)
    check_out = today + timedelta(days=3)
    
    booking = Booking(
        user_id=test_user.id,
        room_id=test_room.id,
        check_in=check_in,
        check_out=check_out,
        total_price=200.0,
        status='confirmed'
    )
    app.db.session.add(booking)
    app.db.session.commit()
    
    assert booking.user_id == test_user.id
    assert booking.room_id == test_room.id
    assert booking.status == 'confirmed'
    assert booking.total_price == 200.0

def test_room_availability(app, test_room, test_user):
    """Test room availability check."""
    # Initially available
    assert test_room.is_available == True
    
    # Create a booking
    today = datetime.now().date()
    booking = Booking(
        user_id=test_user.id,
        room_id=test_room.id,
        check_in=today + timedelta(days=1),
        check_out=today + timedelta(days=3),
        total_price=200.0,
        status='confirmed'
    )
    app.db.session.add(booking)
    app.db.session.commit()
    
    # Room should still be available (is_available flag unchanged)
    assert test_room.is_available == True