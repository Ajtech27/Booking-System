from app import create_app, db
from app.models import Room

app = create_app()

with app.app_context():
    # Check if rooms already exist
    if Room.query.count() == 0:
        rooms = [
            Room(room_number='101', room_type='Single', price_per_night=80, capacity=1, description='Cozy single room with city view', is_available=True),
            Room(room_number='102', room_type='Double', price_per_night=120, capacity=2, description='Spacious double room with en-suite bathroom', is_available=True),
            Room(room_number='103', room_type='Suite', price_per_night=200, capacity=3, description='Luxury suite with living area and balcony', is_available=True),
            Room(room_number='104', room_type='Double', price_per_night=130, capacity=2, description='Ocean view double room', is_available=True),
            Room(room_number='105', room_type='Single', price_per_night=85, capacity=1, description='Quiet single room with garden view', is_available=True),
        ]
        db.session.add_all(rooms)
        db.session.commit()
        print("✅ Sample rooms added to the database!")
    else:
        print("ℹ️ Rooms already exist. Skipping seed.")

print("✅ Database seeded successfully!")