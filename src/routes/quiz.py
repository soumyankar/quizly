import time
import json
import sys
sys.path.append("..")

from flask import Flask, request, redirect, url_for, Blueprint, render_template

from flask_sqlalchemy import SQLAlchemy

from src.models import Admin
from src.extensions import db, login_manager

quiz = Blueprint("/quiz/", __name__, static_folder="../../static", template_folder="../../templates")

@quiz.route("/quiz/", methods=['GET', 'POST'])
def quizhomepage():
	return render_template('quiz.html')