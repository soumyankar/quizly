from flask import Flask, request, redirect, url_for, Blueprint, render_template, flash, abort
from app.models.models import QuizSubscriber, QuizOwner, QuizMaster, UserProfile, User, Quiz
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_user import roles_required
from app.forms.quizforms import UserQuizOwnerActionForm
from app import db

user_dashboard = Blueprint("user_dashboard", __name__, static_folder="static", template_folder="templates")

@user_dashboard.route('/user/dashboard/', methods=['POST','GET'])
@login_required
def user_dashboard_page():
	user = current_user
	user_profile = UserProfile.query.filter(UserProfile.user_id == user.id).first()
	if not user_profile or user_profile.profile_complete == False:
		flash('You need to  <a href="'+url_for('user.edit_user_profile')+'"> complete your profile </a> before you can <b>Create a Quiz</b> or <b>Subscribe to a Quiz</b>.', 'error')
	return render_template('user/user_homepage.html', user=user)

@user_dashboard.route('/user/profile/<username>', methods=['GET'])
def user_profile_page(username):
	user = User.query.filter(User.username == username).first()
	if not user:
		abort(404, description ='The User you are looking for does not exist.') 
	user_profile = UserProfile.query.filter(UserProfile.user_id == user.id).first()
	if not user_profile or user_profile.profile_complete == False:
		abort(404, description ='Looks like this User has not completed their profile page yet.') 

	return render_template('user/user_profile.html', user=user)

@user_dashboard.route('/user/quiz/owned', methods=['POST', 'GET'])
@login_required
def user_quiz_owned():
	user = current_user
	owned_quizzes = QuizOwner.query.filter(QuizOwner.user_id == current_user.id).all()
	return render_template('user/user_quiz_owned.html', user=current_user, owned_quizzes=owned_quizzes)

@user_dashboard.route('/user/quiz/subscribed', methods=['POST', 'GET'])
@login_required
def user_quiz_subscribed():
	user = current_user
	subscribed_quizzes = QuizSubscriber.query.filter(QuizSubscriber.user_id == current_user.id).all()
	return render_template('user/user_quiz_subscribed.html', user=current_user, subscribed_quizzes=subscribed_quizzes)

@user_dashboard.route('/user/quiz/quiz_master', methods=['POST', 'GET'])
@login_required
def user_quiz_master():
	user = current_user
	hosted_quizzes = QuizMaster.query.filter(QuizMaster.user_id == current_user.id).all()
	return render_template('user/user_quiz_master.html', user=current_user, hosted_quizzes=hosted_quizzes)

@user_dashboard.route('/user/quiz/owned/<uuid>', methods=['GET', 'POST'])
@login_required
def user_quiz_owned_actions(uuid):
	user = current_user
	quiz = Quiz.query.filter(Quiz.uuid == uuid).first()
	quiz_owner = quiz.quiz_owner
	if not quiz_owner.user_id == user.id:
		flash('It looks like you do not own this quiz.', 'info')
		return redirect(request.referrer)
	form = UserQuizOwnerActionForm()
	form.quiz_master.choices = [(user.id, user.email) for user in User.query.all()]
	return render_template('user/user_quiz_owned_actions.html', user=user, quiz=quiz, form=form)