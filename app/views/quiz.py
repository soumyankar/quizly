import time
import json
import sys

from flask import Flask, request, redirect, url_for, Blueprint, render_template

from flask_sqlalchemy import SQLAlchemy

from app import db

quiz = Blueprint("/quiz/", __name__, static_folder="../../static", template_folder="../../templates")

@quiz.route("/quiz/", methods=['GET', 'POST'])
def quizhomepage():
	return render_template('quiz/quiz.html')

@quiz.route("/quiz/plans/create", methods=['GET', 'POST'])
def quizcreatepage():
	plan = request.args.get('plan', None)
	return render_template('quiz/quizcreate.html')

@quiz.route("/quiz/register", methods=['GET', 'POST'])
def quizregisterPage():
	return render_template('quiz/quizregister.html')

@quiz.route("/quiz/plans", methods=['GET', 'POST'])
def quizplanspage():
	return render_template('quiz/quizplans.html')