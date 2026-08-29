from flask import Blueprint, render_template
from app.models import Room

rooms_bp = Blueprint('rooms', __name__)

@rooms_bp.route('/')
def list_rooms():
    rooms = Room.query.filter_by(is_available=True).all()
    return render_template('rooms/list.html', rooms=rooms)

@rooms_bp.route('/<int:room_id>')
def detail(room_id):
    room = Room.query.get_or_404(room_id)
    return render_template('rooms/detail.html', room=room)