import time
import json
import sys
sys.path.append("..")

from flask import Flask, request, redirect, url_for, Blueprint, render_template

from flask_sqlalchemy import SQLAlchemy

from src.models import Admin
from src.extensions import db, login_manager

quizcreate = Blueprint("/quiz/plans/create", __name__, static_folder="../../static", template_folder="../../templates")

@quizcreate.route("/quiz/plans/create", methods=['GET', 'POST'])
def quizcreatepage():
	plan = request.args.get('plan', None)
	return render_template('quizcreate.html')