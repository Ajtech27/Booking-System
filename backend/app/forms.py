from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, BooleanField, PasswordField, SubmitField, SelectField, DateField, FloatField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered.')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class BookingForm(FlaskForm):
    check_in = DateField('Check-in Date', validators=[DataRequired()])
    check_out = DateField('Check-out Date', validators=[DataRequired()])
    submit = SubmitField('Book Now')


class RoomForm(FlaskForm):
    room_number = StringField('Room Number', validators=[DataRequired()])
    room_type = SelectField('Room Type', choices=[('Single', 'Single'), ('Double', 'Double'), ('Suite', 'Suite')], validators=[DataRequired()])
    price_per_night = FloatField('Price per Night', validators=[DataRequired()])
    description = TextAreaField('Description')
    capacity = SelectField('Capacity', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4')], validators=[DataRequired()])
    is_available = BooleanField('Available', validators=[DataRequired()])  #SelectField('Available', choices=[(True, 'Yes'), (False, 'No')], validators=[DataRequired()])
    submit = SubmitField('Save Room')