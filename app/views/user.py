from flask import Flask, request, redirect, url_for, Blueprint, render_template, flash, abort
from app.models.models import QuizSubscriber, QuizOwner, QuizMaster, UserProfile, User, Quiz
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_user import roles_required
from app.forms.quizforms import UserQuizOwnerActionForm
from app.db_commands.user_commands import *
from app.db_commands.quiz_commands import *
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
	owned_quizzes = current_user.quizzes_owned
	return render_template('user/user_quiz_owned.html', user=current_user, owned_quizzes=owned_quizzes)

@user_dashboard.route('/user/quiz/subscribed', methods=['POST', 'GET'])
@login_required
def user_quiz_subscribed():
	subscribed_quizzes = current_user.subscriptions
	return render_template('user/user_quiz_subscribed.html', user=current_user, subscribed_quizzes=subscribed_quizzes)

@user_dashboard.route('/user/quiz/quiz_master', methods=['POST', 'GET'])
@login_required
def user_quiz_master():
	hosted_quizzes = current_user.quizzes_hosted
	return render_template('user/user_quiz_master.html', user=current_user, hosted_quizzes=hosted_quizzes)

@user_dashboard.route('/user/quiz/owned/<uuid>', methods=['GET', 'POST'])
@login_required
def user_quiz_owned_actions(uuid):
	form = UserQuizOwnerActionForm()
	form.quiz_master.choices = get_quiz_master_choices_for_uuid(uuid)
	if request.method == 'POST':
		if form.validate():
			if create_quiz_details(form, current_user, uuid):
				flash('Details updated succesfully!', 'success')
				return redirect(url_for('user_dashboard.user_quiz_owned_actions', uuid=uuid))
			else:
				flash('Something went wrong while updating your quiz details :/', 'error')
				return redirect(url_for('user_dashboard.user_quiz_owned_actions', uuid=uuid))

	quiz = get_quiz_for_uuid(uuid)
	if not quiz:
		flash('Could find not quiz against UUID='+uuid, 'error')
		return redirect(url_for('user_dashboard.user_quiz_owned'))
	quiz_owner = quiz.quiz_owner
	if not quiz_owner.user_id == current_user.id:
		flash('It looks like you do not own this quiz.', 'info')
		return redirect(url_for('user_dashboard.user_quiz_owned'))
	return render_template('user/user_quiz_owned_actions.html', user=current_user, quiz=quiz, form=form)

@user_dashboard.route('/user/quiz/quiz_master/<uuid>', methods=['POST', 'GET'])
@login_required
def user_quiz_hosted_actions(uuid):
	quiz = get_quiz_for_uuid(uuid)
	if not quiz:
		flash('No such quiz exists. BAD UUID='+str(uuid), 'error')
		return redirect(url_for('user_dashboard.user_quiz_master'))
	if not master_exists_in_quiz(current_user, quiz):
		flash('You do not seem to be the quiz master of this quiz.', 'error')
		return redirect(url_for('user_dashboard.user_quiz_master'))

	quiz_master = get_quiz_master_for_user_id(current_user, quiz)
	return render_template('user/user_quiz_master_actions.html', user=current_user, quiz=quiz, quiz_master=quiz_master)

@user_dashboard.route('/user/quiz/owned/receipt/<uuid>', methods=['GET'])
@login_required
def user_quiz_owned_receipt(uuid):
	quiz = get_quiz_for_uuid(uuid)
	if not quiz:
		flash('Something went wrong. We could not find this quiz :/', 'error')
		return redirect(url_for('user_dashboard.user_quiz_owned'))
	quiz_owner = QuizOwner.query.filter(QuizOwner.quiz_id == quiz.id).first()
	if not quiz_owner:
		flash('Something went wrong. We could find the owner of this quiz.', 'error')
		return redirect(url_for('user_dashboard.user_quiz_owned'))
	if not quiz_owner.user_id == current_user.id:
		flash('You do not seem to be the owner of this quiz.', 'error')
		return redirect(url_for('user_dashboard.user_quiz_owned'))

	description = "Quiz Creation fee for Quiz UUID: "+str(quiz.id)
	razorpay_payment_keys = {"razorpay_payment_id": quiz_owner.razorpay_payment_id, "razorpay_order_id": quiz_owner.razorpay_order_id, "razorpay_signature": quiz_owner.razorpay_signature}
	return render_template('razorpay/payment_invoice.html', payment_state=True, description=description, client=quiz.quiz_owner, params_dict=razorpay_payment_keys, quiz=quiz)

@user_dashboard.route('/user/quiz/subscribed/<uuid>', methods=['GET', 'POST'])
@login_required
def user_quiz_subscribed_actions(uuid):
	quiz = get_quiz_for_uuid(uuid)
	if not quiz:
		flash('No such quiz exists. BAD UUID='+str(uuid), 'error')
		return redirect(request.referrer)

	if not subscriber_exists_in_quiz(current_user, quiz):
		flash('You are not subscribed to this quiz.', 'error')
		return redirect(request.referrer)
	subscriber = get_subscriber_for_user_id(current_user, quiz)

	return render_template('user/user_quiz_subscribed_actions.html', user=current_user, quiz=quiz, subscriber=subscriber)

@user_dashboard.route('/user/quiz/subscribed/receipt/<uuid>', methods=['GET'])
@login_required
def user_quiz_subscribed_receipt(uuid):
	quiz = get_quiz_for_uuid(uuid)
	if not quiz:
		flash('We could not find this quiz :/', 'error')
		return redirect(url_for('user_dashboard.user_quiz_subscribed'))
	sub = get_subscriber_for_user_id(current_user, quiz)
	if not sub:
		flash('You dont seem to be subscribed to this quiz.', 'error')
		return redirect(url_for('user_dashboard.user_quiz_subscribed'))

	description = "Quiz Subscription Fee for Quiz UUID: "+str(quiz.id)
	razorpay_payment_keys = {"razorpay_payment_id": sub.razorpay_payment_id, "razorpay_order_id": sub.razorpay_order_id, "razorpay_signature": sub.razorpay_signature}
	return render_template('razorpay/payment_invoice.html', payment_state=True, description=description, client=sub, params_dict=razorpay_payment_keys, quiz=quiz)

