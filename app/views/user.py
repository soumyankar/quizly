from flask import Flask, request, redirect, url_for, Blueprint, render_template

from app.models.models import QuizSubscriber, QuizOwner, QuizMaster
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_user import roles_required
from app import db

user_dashboard = Blueprint("user_dashboard", __name__, static_folder="static", template_folder="templates")

@user_dashboard.route('/user/dashboard/', methods=['POST','GET'])
@login_required
def user_dashboard_page():
	user = current_user
	return render_template('user/user_homepage.html', user=user)

# @user_dashboard.route('/user/settings/edit_user_profile', methods=['POST', 'GET'])
# @login_required
# def user_settings_edit_profile_page():
# 	user = current_user
# 	return render_template('user/user_settings.html', user=user)

@user_dashboard.route('/user/quiz/owned', methods=['POST', 'GET'])
@login_required
def user_quiz_owned():
	user = current_user
	owned_quizzes = QuizOwner.query.filter(QuizOwner.user_id == current_user.id).all()
	return render_template('user/user_quiz_owned.html', owned_quizzes=owned_quizzes)

@user_dashboard.route('/user/quiz/subscribed', methods=['POST', 'GET'])
@login_required
def user_quiz_subscribed():
	user = current_user
	subscribed_quizzes = QuizSubscriber.query.filter(QuizSubscriber.user_id == current_user.id).all()
	return render_template('user/user_quiz_subscribed.html', subscribed_quizzes=subscribed_quizzes)

@user_dashboard.route('/user/quiz/quiz_master', methods=['POST', 'GET'])
@login_required
def user_quiz_master():
	user = current_user
	hosted_quizzes = QuizMaster.query.filter(QuizMaster.user_id == current_user.id).all()
	return render_template('user/user_quiz_master.html', hosted_quizzes=hosted_quizzes)