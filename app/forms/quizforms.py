from app import db
try:
    from flask_wtf import FlaskForm             # Try Flask-WTF v0.13+
except ImportError:
    from flask_wtf import Form as FlaskForm     # Fallback to Flask-WTF v0.12 or older
from wtforms import StringField, PasswordField, BooleanField, SelectField, TextField, IntegerField, SubmitField, HiddenField, TimeField, DateField, SelectMultipleField
from wtforms import validators, ValidationError
from wtforms.validators import InputRequired, Email, Length
from app.models.models import User
from datetime import date, datetime


today = date.today()
current_time = datetime.now().time()

def date_validator(form, field):

    if field.data < today:
        raise ValidationError('Past Date cannot be selected')


from wtforms.fields import StringField


class TagListField(StringField):
    """Stringfield for a list of separated tags"""

    def __init__(self, label='', validators=None, remove_duplicates=True, to_lowercase=True, separator=' ', **kwargs):
        """
        Construct a new field.
        :param label: The label of the field.
        :param validators: A sequence of validators to call when validate is called.
        :param remove_duplicates: Remove duplicates in a case insensitive manner.
        :param to_lowercase: Cast all values to lowercase.
        :param separator: The separator that splits the individual tags.
        """
        super(TagListField, self).__init__(label, validators, **kwargs)
        self.remove_duplicates = remove_duplicates
        self.to_lowercase = to_lowercase
        self.separator = separator
        self.data = []

    def _value(self):
        if self.data:
            return u', '.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split(self.separator)]
            if self.remove_duplicates:
                self.data = list(self._remove_duplicates(self.data))
            if self.to_lowercase:
                self.data = [x.lower() for x in self.data]

    @classmethod
    def _remove_duplicates(cls, seq):
        """Remove duplicates in a case insensitive, but case preserving manner"""
        d = {}
        for item in seq:
            if item.lower() not in d:
                d[item.lower()] = True
                yield item

# def time_validator(form, field):
#     if field.data < current_time:
#         raise ValidationError('Past Time cannot be selected')

class QuizCreateForm(FlaskForm):
    plan = SelectField('Plan', choices="", render_kw = {"disabled": "disabled"})
    submit = SubmitField(('Create Quiz'))

class QuizCreateEditForm(FlaskForm):
    name = StringField('Quiz Name', validators=[InputRequired()])
    date = DateField('Quiz Date', validators=[InputRequired(), date_validator])
    time = TimeField('Time', validators=[InputRequired()])
    subscription_price = IntegerField('User Registration Price', validators=[InputRequired()])
    quiz_master = SelectField('Quiz Master', choices="", validators=[InputRequired()])
    submit = SubmitField(('Create Quiz'))

class UserQuizOwnerActionForm(FlaskForm):

    name = StringField('Quiz Name', validators=[InputRequired()])
    date = DateField('Quiz Date', validators=[InputRequired(), date_validator])
    time = TimeField('Time', validators=[InputRequired()])
    tags = TagListField("Tags", separator=",", validators=[Length(max=8, message="You can only use up to 8 tags.")])
    # tags = SelectMultipleField(u'Categories', choices=[('1','M.E.L.A'), ('2','H.E.L.M'), ('3', 'spEnt'), ('4', 'General'), ('5', 'Sports'), ('6' , 'Pop Culture'),('7','Sci-tech'), ('8', 'Tech'), ('9', 'Misc') ], validators=[InputRequired()], render_kw={"multiple": "multiple"})
    subscription_price = IntegerField('User Registration Price', validators=[InputRequired()])
    quiz_master = SelectField('Quiz Master', choices="", validators=[InputRequired()], render_kw = {"class":"form-control"})
    submit = SubmitField(('Create Quiz'))