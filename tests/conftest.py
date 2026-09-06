import pytest
from app import create_app, db
from app.models import User, Room, Booking

@pytest.fixture
def app():
    """Create and configure a test app instance."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Test client for making requests."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Test CLI runner."""
    return app.test_cli_runner()

@pytest.fixture
def test_user(app):
    """Create a test user."""
    user = User(
        username='testuser',
        email='test@example.com',
        password_hash='$2b$12$testhash',
        role='user'
    )
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def test_admin(app):
    """Create a test admin."""
    admin = User(
        username='admin',
        email='admin@example.com',
        password_hash='$2b$12$testhash',
        role='admin'
    )
    db.session.add(admin)
    db.session.commit()
    return admin

@pytest.fixture
def test_room(app):
    """Create a test room."""
    room = Room(
        room_number='101',
        room_type='Single',
        price_per_night=100.0,
        description='Test room',
        capacity=2,
        is_available=True
    )
    db.session.add(room)
    db.session.commit()
    return room