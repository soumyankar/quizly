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

quizcreate = Blueprint("/quiz/create", __name__, static_folder="../../static", template_folder="../../templates")

@quizcreate.route("/quiz/create", methods=['GET', 'POST'])
def quizregisterPage():
	return render_template('quizcreate.html')