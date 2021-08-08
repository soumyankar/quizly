import json
from flask import Flask, request, redirect, url_for, Blueprint, render_template, flash, abort
from app.models.models import QuizSubscriber, QuizOwner, QuizMaster, UserProfile, User, Quiz
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_user import roles_required
from app.forms.quizforms import UserQuizOwnerActionForm
from app.db_commands.user_commands import *
from app.db_commands.quiz_commands import *
from app import db, csrf_protect

user_dashboard = Blueprint("user_dashboard", __name__, static_folder="static", template_folder="templates")

@user_dashboard.route('/user/dashboard/', methods=['POST','GET'])
@login_required
def user_dashboard_page():
	if not user_profile_exists(current_user):
		flash('You need to  <a href="'+url_for('user.edit_user_profile')+'"> complete your profile </a> before you can <b>Create a Quiz</b> or <b>Subscribe to a Quiz</b>.', 'error')
	return render_template('user/user_homepage.html', user=current_user)

@user_dashboard.route('/user/profile/<username>', methods=['GET'])
def user_profile_page(username):
	if not user_exists(username):
		abort(404, description ='The User you are looking for does not exist.')
	user = get_user_for_username(username) 
	if not user_profile_exists(user):
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
	quiz = get_quiz_for_uuid(uuid)
	if not quiz:
		flash('Could find not quiz against UUID='+uuid, 'error')
		return redirect(url_for('user_dashboard.user_quiz_owned'))
	if quiz.quiz_owner.payment_status == False:
		flash('You still need to complete your quiz payment', 'error')
		return redirect(url_for('quiz.quiz_create_payment_page', uuid=quiz.id))
	if not quiz.quiz_owner.user_id == current_user.id:
		flash('It looks like you do not own this quiz.', 'info')
		return redirect(url_for('user_dashboard.user_quiz_owned'))

	form = UserQuizOwnerActionForm(obj=quiz.details)
	form.quiz_master.choices = get_quiz_master_choices_for_uuid(uuid)
	if request.method == 'POST':
		if form.validate():
			if create_quiz_details(form, uuid):
				flash('Details updated succesfully!', 'success')
				return redirect(url_for('user_dashboard.user_quiz_owned_actions', uuid=uuid))
			else:
				flash('Something went wrong while updating your quiz details :/', 'error')
				return redirect(url_for('user_dashboard.user_quiz_owned_actions', uuid=uuid))

	return render_template('user/user_quiz_owned_actions.html', user=current_user, quiz=quiz, form=form)

@user_dashboard.route('/user/quiz/owned/deactivate', methods=['POST'])
@login_required
@csrf_protect.exempt
def user_quiz_owned_actions_deactivate():
	request_data = request.get_json()
	user_id = request_data['user_id']
	quiz_uuid = request_data['quiz_uuid']
	quiz = get_quiz_for_uuid(quiz_uuid)
	if not quiz:
		abort(500)
	try:
		resp = quiz_deactivate(quiz)
		if resp:
			return json.dumps(resp, default=str)
		else:
			resp = {"status": "500"}
			return json.dumps(resp, default=str)
	except Exception as e:
		print (e)
		abort(500)

@user_dashboard.route('/user/quiz/owned/forgive_payment', methods=['POST'])
@login_required
@csrf_protect.exempt
def user_quiz_owned_actions_forgive():
	request_data = request.get_json()
	user_id = request_data['user_id']
	quiz_uuid = request_data['quiz_uuid']
	user_subscriber = get_user_for_id(user_id)
	quiz = get_quiz_for_uuid(quiz_uuid)
	if not quiz:
		flash('Something went wrong with quiz uuid.')
		abort(500)
	if total_player_exceeded(quiz):
		flash('The quiz is already full. Forgiving payment consumes another slot.')
	subscriber = get_subscriber_for_user_id(user_subscriber, quiz)
	if not subscriber:
		flash('Could not find this subscriber in this quiz.')
		abort(500)
	try:
		resp = quiz_forgive_payment(subscriber, quiz)
		if resp:
			return json.dumps(resp, default=str)
		else:
			abort(500)
	except Exception as e:
		print(e)
		abort(500)

@user_dashboard.route('/user/quiz/owned/kick', methods=['POST'])
@login_required
@csrf_protect.exempt
def user_quiz_owned_actions_kick():
	request_data = request.get_json()
	user_id = request_data['user_id']
	quiz_uuid = request_data['quiz_uuid']
	user_subscriber = get_user_for_id(user_id)
	quiz = get_quiz_for_uuid(quiz_uuid)
	if not quiz:
		flash('Something went wrong with quiz uuid.')
		abort(500)
	subscriber = get_subscriber_for_user_id(user_subscriber, quiz)
	if not subscriber:
		flash('Could not find this subscriber in this quiz.')
		abort(500)
	try:
		if kick_subscriber_from_quiz(subscriber, quiz):
			resp ={"status": "OK"}
			return json.dumps(resp, default=str)
		resp = {"status": "500"}
		return json.dumps(resp, default=str)
	except Exception as e:
		print(e)
		abort(500)

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

@user_dashboard.route('/user/quiz/quiz_master/user_confirm', methods=['POST'])
@login_required
@csrf_protect.exempt
def user_quiz_master_toggle_status():
	request_data = request.get_json()
	user_id = request_data['user_id']
	quiz_uuid = request_data['quiz_uuid']
	quiz = get_quiz_for_uuid(quiz_uuid)
	if not master_exists_in_quiz(current_user, quiz):
		abort(500)
	try:
		resp = quiz_master_toggle_status(current_user, quiz)
		return json.dumps(resp, default=str)
	except Exception as e:
		print(e)
		abort(500)

@user_dashboard.route('/user/quiz/subscriber/user_confirm', methods=['POST'])
@login_required
@csrf_protect.exempt
def user_quiz_subscriber_toggle_status():
	request_data = request.get_json()
	user_id = request_data['user_id']
	quiz_uuid = request_data['quiz_uuid']
	quiz = get_quiz_for_uuid(quiz_uuid)
	if not subscriber_exists_in_quiz(current_user, quiz):
		abort(500)
	try:
		resp = quiz_subscriber_toggle_status(current_user, quiz)
		return json.dumps(resp, default=str)
	except Exception as e:
		print(e)
		abort(500)

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

