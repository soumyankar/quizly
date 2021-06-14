import time
import json
import sys
sys.path.append("..")

from flask import Flask, request, redirect, url_for, Blueprint, render_template

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from src.models import Admin
from src.extensions import db, login_manager

adminlogin = Blueprint("adminlogin", __name__, static_folder="../../static", template_folder="../../templates")


class LoginForm(FlaskForm):
	username = StringField('username', validators=[InputRequired()])
	password = PasswordField('password', validators=[InputRequired()])

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



