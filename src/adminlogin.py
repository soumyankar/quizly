from flask import Flask, request, redirect, url_for, Blueprint, render_template

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

import time
import json
adminlogin = Blueprint("adminLogin", __name__, static_folder="../static", template_folder="../templates")
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'adminLoginPage'

class Admin(UserMixin, db.Model):
	id=db.Column(db.Integer, primary_key=True)
	username=db.Column(db.String(15),unique=True)
	email=db.Column(db.String(80),unique=True)
	password=db.Column(db.String(80))
	date_created=db.Column(db.DateTime, default=datetime.now())
	
	def __repr__(self):
		return '<Admin %r>' % self.id

class LoginForm(FlaskForm):
	username = StringField('username', validators=[InputRequired()])
	password = PasswordField('password', validators=[InputRequired()])

@login_manager.user_loader
def load_user(user_id):
	return Admin.query.get((user_id))

@adminlogin.route("/adminlogin", methods=['GET', 'POST'])
def adminloginPage():
	if current_user.is_authenticated:
		return 'This worked!'
		flash('You are already logged in my dude')
	form = LoginForm()
	if form.validate_on_submit():
		user = Admin.query.filter_by(username=form.username.data).first()
		if user:
			if user.password == form.password.data:
				login_user(user,remember=False)
				return 'This worked!'
			else:
				return '<h1>Wrong Password</h1>'
		else:
			return '<h1>Username or password is invalid.</h1>'
	return render_template('adminlogin.html', form=form)



