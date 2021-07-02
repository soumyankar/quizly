from app import db
try:
    from flask_wtf import FlaskForm             # Try Flask-WTF v0.13+
except ImportError:
    from flask_wtf import Form as FlaskForm     # Fallback to Flask-WTF v0.12 or older
from wtforms import StringField, PasswordField, BooleanField, SelectField, TextField, IntegerField, SubmitField, HiddenField, TimeField, DateField
from wtforms import validators, ValidationError
from wtforms.validators import InputRequired, Email, Length
from app.models.models import User
from datetime import date, datetime


today = date.today()
current_time = datetime.now().time()
print(current_time)
print(today)

def date_validator(form, field):

    if field.data < today:
        raise ValidationError('Past Date cannot be selected')


def time_validator(form, field):
    if field.data < current_time:
        raise ValidationError('Past Time cannot be selected')

class QuizRegisterForm(FlaskForm):

    name = StringField('Quiz Name', validators=[InputRequired()])
    date = DateField('Quiz Date', default=today , validators=[InputRequired(), date_validator])
    time = TimeField('Time', default=current_time, validators=[InputRequired(), time_validator])
    subscription_price = IntegerField('User Registration Price', validators=[InputRequired()])
    quiz_master = SelectField('Quiz Master', choices="", validators=[InputRequired()], render_kw = {"class":"form-control"})

