from flask_user import UserMixin
from app import db
from datetime import datetime
from wtforms import StringField, PasswordField, BooleanField, SelectField, TextField, IntegerField, SubmitField
from wtforms import validators, ValidationError
from wtforms.validators import InputRequired, Email, Length
from flask_wtf import FlaskForm 

class Admin(UserMixin, db.Model):
	__tablename__ = 'admin'
	id=db.Column(db.Integer, primary_key=True)
	username=db.Column(db.String(15),unique=True)
	email=db.Column(db.String(80),unique=True)
	password=db.Column(db.String(80))
	date_created=db.Column(db.DateTime, default=datetime.now())
	
	def __repr__(self):
		return '<Admin %r>' % self.id

# Define User data-model
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    # User Authentication fields
    email = db.Column(db.String(255), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    email_confirmed_at = db.Column(db.DateTime, nullable=True)

    # User fields
    active = db.Column(db.Boolean(), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    nationality = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    gender = db.Column(db.String(50), nullable=False)

    # Relationships
    roles = db.relationship('Role', secondary='users_roles',
                            backref=db.backref('users', lazy='dynamic'))

# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, server_default=u'', unique=True)
    label = db.Column(db.Unicode(255), server_default=u'')  # for display purposes

# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'users_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

