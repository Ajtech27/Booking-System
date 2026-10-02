from app import create_app, db
from app.models import User, Room
from flask_bcrypt import bcrypt

app = create_app()

# ✅ Create tables if they don't exist


with app.app_context():
    db.create_all()
    print("✅ Database tables created!")
    
    # Create admin user if none exists
    if not User.query.filter_by(email='admin@hotel.com').first():
        hashed = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin = User(username='admin', email='admin@hotel.com', password_hash=hashed, role='admin')
        db.session.add(admin)
        print("✅ Admin user created!")
    
    # Create sample rooms if none exist
    if Room.query.count() == 0:
        rooms = [
             Room(room_number='101', room_type='Single', price_per_night=80, capacity=1, description='Cozy single room with city view', is_available=True),
                        Room(room_number='102', room_type='Double', price_per_night=120, capacity=2, description='Spacious double room with en-suite bathroom', is_available=True),
                        Room(room_number='103', room_type='Suite', price_per_night=200, capacity=3, description='Luxury suite with living area and balcony', is_available=True),
                        Room(room_number='104', room_type='Double', price_per_night=130, capacity=2, description='Ocean view double room', is_available=True),
                        Room(room_number='105', room_type='Single', price_per_night=85, capacity=1, description='Quiet single room with garden view', is_available=True),
        ]
        db.session.add_all(rooms)
        print(f"✅ {len(rooms)} sample rooms created!")
    
    db.session.commit()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
