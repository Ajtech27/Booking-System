from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Room, Booking
from app.forms import BookingForm
from datetime import datetime, timedelta 

bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('/book/<int:room_id>', methods=['GET', 'POST'])
@login_required
def book_room(room_id):
    room = Room.query.get_or_404(room_id)
    
    if not room.is_available:
        flash('This room is not available.', 'danger')
        return redirect(url_for('rooms.detail', room_id=room.id))
    
    form = BookingForm()
    
    if form.validate_on_submit():
        check_in = form.check_in.data
        check_out = form.check_out.data
        
        # Validate dates
        if check_in < datetime.now().date():
            flash('Check-in date must be today or in the future.', 'danger')
            return render_template('bookings/book.html', form=form, room=room)
        
        if check_out <= check_in:
            flash('Check-out date must be after check-in date.', 'danger')
            return render_template('bookings/book.html', form=form, room=room)
        
        # Check if room is available for the selected dates
        conflicting_booking = Booking.query.filter(
            Booking.room_id == room.id,
            Booking.status != 'cancelled',
            Booking.check_in < check_out,
            Booking.check_out > check_in
        ).first()
        
        if conflicting_booking:
            flash('Room is not available for the selected dates.', 'danger')
            return render_template('bookings/book.html', form=form, room=room)
        
        # Calculate total price
        nights = (check_out - check_in).days
        total_price = nights * room.price_per_night
        
        # Create booking
        booking = Booking(
            user_id=current_user.id,
            room_id=room.id,
            check_in=check_in,
            check_out=check_out,
            total_price=total_price,
            status='confirmed'
        )
        
        db.session.add(booking)
        db.session.commit()
        
        flash('Room booked successfully! Total: ${:.2f}'.format(total_price), 'success')
        return redirect(url_for('bookings.my_bookings'))
    
    return render_template('bookings/book.html', form=form, room=room)


@bookings_bp.route('/my-bookings')
@login_required
def my_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.check_in.desc()).all()
    return render_template('bookings/my_bookings.html', bookings=bookings)


@bookings_bp.route('/cancel/<int:booking_id>', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    if booking.user_id != current_user.id:
        flash('You do not have permission to cancel this booking.', 'danger')
        return redirect(url_for('bookings.my_bookings'))
    
    if booking.status != 'confirmed':
        flash('This booking cannot be cancelled.', 'danger')
        return redirect(url_for('bookings.my_bookings'))
    
    # Check if cancellation is allowed (e.g., at least 24 hours before check-in)
    now = datetime.now().date()
    days_until_checkin = (booking.check_in - now).days
    
    if days_until_checkin < 1:
        flash('Bookings can only be cancelled at least 1 day before check-in.', 'danger')
        return redirect(url_for('bookings.my_bookings'))
    
    booking.status = 'cancelled'
    db.session.commit()
    
    flash('Booking cancelled successfully.', 'success')
    return redirect(url_for('bookings.my_bookings'))