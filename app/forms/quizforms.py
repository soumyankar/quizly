from app import db
try:
    from flask_wtf import FlaskForm             # Try Flask-WTF v0.13+
except ImportError:
    from flask_wtf import Form as FlaskForm     # Fallback to Flask-WTF v0.12 or older
from wtforms import StringField, PasswordField, BooleanField, SelectField, TextField, IntegerField, SubmitField, HiddenField, TimeField, DateField
from wtforms import validators, ValidationError
from wtforms.validators import InputRequired, Email, Length
from app.models.models import User

class QuizRegisterForm(FlaskForm):

    name = StringField('Quiz Name', validators=[InputRequired()])
    date = DateField('Quiz Date', validators=[InputRequired()])
    time = TimeField('Time', validators=[InputRequired()])
    subscription_price = IntegerField('User Registration Price', validators=[InputRequired()])
    quiz_master = SelectField('Quiz Master', choices="", validators=[InputRequired()], render_kw = {"class":"form-control"})