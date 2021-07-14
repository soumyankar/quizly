import pycountry
import phonenumbers
from phonenumbers.phonenumberutil import country_code_for_region
# Flask-WTF v0.13 renamed Flask to FlaskForm
try:
    from flask_wtf import FlaskForm             # Try Flask-WTF v0.13+
except ImportError:
    from flask_wtf import Form as FlaskForm     # Fallback to Flask-WTF v0.12 or older
from app.user_manager import CustomUserManager
from wtforms import StringField, PasswordField, BooleanField, SelectField, TextField, IntegerField, SubmitField, HiddenField, DateField
from wtforms import validators, ValidationError
from wtforms.validators import InputRequired, Email, Length
from app.models.models import User
from datetime import date, datetime

nationalityCountries = []
country_codes_alpha_2 = []
for country in pycountry.countries:
    nationalityCountries.append(country.name)
    # country_codes_alpha_2.append( ("(+",phonenumbers.country_code_for_region(country.alpha_2),") ", country.alpha_2), (phonenumbers.country_code_for_region(country.alpha_2)) )
    # country_codes_alpha_2.append(phonenumbers.country_code_for_region(country.alpha_2))

def unique_username_validator(form, field):
    if (User.query.filter_by(username=field.data).first()):
        raise ValidationError('Username already exists. Try using some other username.')

def unique_email_validator(form, field):
    if (User.query.filter_by(email=field.data).first()):
        raise ValidationError('Email Address already exists.')

def password_validator(form, field):
    """Ensure that passwords have at least 6 characters with one lowercase letter, one uppercase letter and one number. """

    # Convert string to list of characters
    password = list(field.data)
    password_length = len(password)

    # Count lowercase, uppercase and numbers
    lowers = uppers = digits = 0
    for ch in password:
        if ch.islower(): lowers += 1
        if ch.isupper(): uppers += 1
        if ch.isdigit(): digits += 1

    # Password must have one lowercase letter, one uppercase letter and one digit
    is_valid = password_length >= 6 and lowers and uppers and digits
    if not is_valid:
        raise ValidationError(
            ('Password must have at least 6 characters with one lowercase letter, one uppercase letter and one number'))

def date_validator(form, field):
    today = date.today()
    if field.data > today:
        raise ValidationError('Future Date cannot be selected')


from flask_user.forms import RegisterForm
class CustomRegisterForm(FlaskForm):
    next = HiddenField()        # for login_or_register.html
    reg_next = HiddenField()    # for register.html
    username = StringField(('Username'), validators=[
        validators.DataRequired(('Username is required')),
        unique_username_validator
        ])
    email = StringField(('Email'), validators=[
        unique_email_validator,
        InputRequired(),
        Email()
        ])
    password = PasswordField(('Password'), validators=[
        InputRequired()])
    retype_password = PasswordField(('Retype Password'), validators=[
        validators.EqualTo('password', message=('Password and Retype Password did not match'))])
    invite_token = HiddenField(('Token'))
    submit = SubmitField('Register')

 

# Customize the User profile form:
from flask_user.forms import EditUserProfileForm
class CustomUserProfileForm(FlaskForm):
    first_name = StringField('First name', validators=[InputRequired('First name is required')])
    last_name = StringField('Last name', validators=[InputRequired('Last name is required')])
    nationality = SelectField('Nationality', choices=nationalityCountries, default="India", validators=[InputRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'),('Female', 'Female'),('Others', 'Choose not to identify')], validators=[InputRequired()])
    institution = StringField('Institution', validators=[InputRequired()])
    dob = DateField('Tell us your Birthday', validators=[InputRequired(), date_validator])
    phone_number = StringField('Phone Number', validators=[InputRequired()])
    phone_number_country_code = SelectField('Code', choices=[(country.alpha_2, (country_code_for_region(country.alpha_2) )) for country in pycountry.countries], validators=[InputRequired()])
    submit = SubmitField('Save')


from flask_user.forms import LoginForm
class CustomLoginForm(FlaskForm):
    next = HiddenField()         # for login.html
    reg_next = HiddenField()     # for login_or_register.html
    email = StringField(('Email'), validators=[
        validators.DataRequired(('Email is required')),
        validators.Email(('Invalid Email'))])
    password = PasswordField('Password', validators=[])
    remember_me = BooleanField(('Remember me'))
    submit = SubmitField(('Sign in'))

from flask_user.forms import ChangePasswordForm
class CustomChangePasswordForm(FlaskForm):
    old_password = PasswordField(('Old Password'), validators=[
        validators.DataRequired(('Old Password is required')),
        ])
    new_password = PasswordField(('New Password'), validators=[
        validators.DataRequired(('New Password is required')),
        password_validator,
        ])
    retype_password = PasswordField(('Retype New Password'), validators=[
        validators.DataRequired(('Retyped password is required')),
        validators.EqualTo('new_password', message=('New Password and Retype Password did not match'))
        ])
    submit = SubmitField(('Change password'))