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

quizplans = Blueprint("/quiz/plans", __name__, static_folder="../../static", template_folder="../../templates")

@quizplans.route("/quiz/plans", methods=['GET', 'POST'])
def quizplanspage():
	return render_template('quizplans.html')