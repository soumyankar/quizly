import pycountry
# Flask-WTF v0.13 renamed Flask to FlaskForm
try:
    from flask_wtf import FlaskForm             # Try Flask-WTF v0.13+
except ImportError:
    from flask_wtf import Form as FlaskForm     # Fallback to Flask-WTF v0.12 or older
from wtforms import StringField, PasswordField, BooleanField, SelectField, TextField, IntegerField, SubmitField, HiddenField
from wtforms import validators, ValidationError
from wtforms.validators import InputRequired, Email, Length

nationalityCountries = []
for country in pycountry.countries:
	nationalityCountries.append(country.name)

# Customize the Register form:
from flask_user.forms import RegisterForm
class CustomRegisterForm(FlaskForm):
    next = HiddenField()        # for login_or_register.html
    reg_next = HiddenField()    # for register.html
    username = StringField(('Username'), validators=[
        validators.DataRequired(('Username is required'))])
    email = StringField(('Email'), validators=[
        InputRequired(),
        Email()])
    password = PasswordField(('Password'), validators=[
        InputRequired()])
    retype_password = PasswordField(('Retype Password'), validators=[
        validators.EqualTo('password', message=('Password and Retype Password did not match'))])
    invite_token = HiddenField(('Token'))

    email = StringField('Email Address', validators=[InputRequired(), Email()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    nationality = SelectField('Nationality', choices=nationalityCountries, validators=[InputRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'),('Female', 'Female'),('Others', 'Choose not to identify')], validators=[InputRequired()])
    age = IntegerField('Age', validators=[InputRequired()])
    submit = SubmitField(('Register'))

# Customize the User profile form:
from flask_user.forms import EditUserProfileForm
class CustomUserProfileForm(FlaskForm):
    first_name = StringField('First name', validators=[
        validators.DataRequired('First name is required')])
    last_name = StringField('Last name', validators=[
        validators.DataRequired('Last name is required')])
    submit = SubmitField('Save')

from flask_user.forms import LoginForm
class CustomLoginForm(FlaskForm):
    next = HiddenField()         # for login.html
    reg_next = HiddenField()     # for login_or_register.html
    email = StringField(('Email'), validators=[
        validators.DataRequired(('Email is required')),
        validators.Email(('Invalid Email'))])

    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField(('Remember me'))
    submit = SubmitField(('Sign in'))