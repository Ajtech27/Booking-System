from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Room, Booking, User
from app.forms import RoomForm

admin_bp = Blueprint('admin', __name__)

# ── Admin Access Decorator ──
def admin_required(func):
    from functools import wraps
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('index'))
        return func(*args, **kwargs)
    return decorated_view


@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    rooms = Room.query.all()
    bookings = Booking.query.all()
    users = User.query.all()
    return render_template('admin/dashboard.html', rooms=rooms, bookings=bookings, users=users)


@admin_bp.route('/add-room', methods=['GET', 'POST'])
@login_required
@admin_required
def add_room():
    form = RoomForm()
    
    if form.validate_on_submit():
        room = Room(
            room_number=form.room_number.data,
            room_type=form.room_type.data,
            price_per_night=form.price_per_night.data,
            description=form.description.data,
            capacity=form.capacity.data,
            is_available=form.is_available.data == 'True' or form.is_available.data == True
        )
        db.session.add(room)
        db.session.commit()
        flash(f'Room {room.room_number} added successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/add_room.html', form=form)


@admin_bp.route('/edit-room/<int:room_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_room(room_id):
    room = Room.query.get_or_404(room_id)
    form = RoomForm(obj=room)
    
    if form.validate_on_submit():
        room.room_number = form.room_number.data
        room.room_type = form.room_type.data
        room.price_per_night = form.price_per_night.data
        room.description = form.description.data
        room.capacity = form.capacity.data
        room.is_available = form.is_available.data == 'True' or form.is_available.data == True
        
        db.session.commit()
        flash(f'Room {room.room_number} updated successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/edit_room.html', form=form, room=room)


@admin_bp.route('/delete-room/<int:room_id>', methods=['POST'])
@login_required
@admin_required
def delete_room(room_id):
    room = Room.query.get_or_404(room_id)
    
    # Check if room has bookings
    if room.bookings:
        flash('Cannot delete room with existing bookings.', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    db.session.delete(room)
    db.session.commit()
    flash(f'Room {room.room_number} deleted successfully.', 'success')
    return redirect(url_for('admin.dashboard'))