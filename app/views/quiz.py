import uuid
import json
from datetime import datetime, date
from app import db, csrf_protect
from app.forms.quizforms import QuizCreateForm
from app.misc.razorpay_creds import RazorpayOrder, razorpay_verify_payment_signature
from app.models.models import PricingPlan, Quiz, User, QuizOwner, QuizMaster, QuizSubscriber, UserProfile
from app.db_commands.quiz_commands import *
from app.decorators.custom_decorators import *
from flask import (Blueprint, Flask, flash, redirect, render_template, request,url_for,abort)
from flask_login import current_user, login_required
from flask_sqlalchemy import SQLAlchemy

quiz = Blueprint("quiz", __name__, static_folder="static", template_folder="templates")

@quiz.route("/quiz/", methods=['GET', 'POST'])
def quiz_homepage():
	return render_template('quiz/quiz.html')

@quiz.route("/quiz/browse", methods=['GET', 'POST'])
def quiz_browse_page():
	quizzes = get_browse_quizzes()
	return render_template('quiz/quiz_browse.html', quizzes=quizzes)

@quiz.route("/quiz/plans", methods=['GET', 'POST'])
def quiz_plans_page():
	pricing_plans = PricingPlan.query.all()
	return render_template('quiz/quiz_plans.html', pricing_plans=pricing_plans)

@quiz.route("/quiz/create/<plan>", methods=['GET','POST'])
@login_required
@profile_required
@csrf_protect.exempt
def quiz_create_page(plan):
	if request.method == 'GET':
		return redirect(url_for('quiz.quiz_plans_page'))

	chosen_plan = PricingPlan.query.filter(PricingPlan.id == plan).first()
	if not chosen_plan:
		flash('That is not a valid plan ID. Choose again')
		return redirect(url_for('quiz.quizplanspage'))

	# form.quiz_master.choices = [(user.id, user.email) for user in User.query.all()]
	new_quiz = create_quiz(chosen_plan, current_user)
	if new_quiz.parent_pricing_plan.payment_required == False:
		razorpay_payment_keys = { "razorpay_payment_id": 'free_plan', "razorpay_order_id": 'free_plan', "razorpay_signature": 'free_plan'}
		add_quiz_owner_payment_details(new_quiz.quiz_owner.id, 0, razorpay_payment_keys)
		return redirect(url_for('user_dashboard.user_quiz_owned_receipt', uuid=new_quiz.id))
	return redirect(url_for('quiz.quiz_create_payment_page', uuid=new_quiz.id))

@quiz.route("/quiz/register/<string:uuid>", methods=['GET', 'POST'])
@login_required
@profile_required
@csrf_protect.exempt
def quiz_register_page(uuid):
	quiz = get_quiz_for_uuid(uuid)
	if not quiz:
		flash('This quiz does not seem to exist', 'error')
		return redirect(url_for('quiz.quiz_browse_page'))

	if request.method == 'POST':
		quiz_owner = quiz.quiz_owner
		if not quiz_owner:
			flash('This quiz does not have a quiz owner. Registration may not be allowed', 'error')
			return redirect(url_for('quiz.quiz_browse_page'))
		if (quiz_owner.user_id == current_user.id):
			flash('You may not register for quizzes you own.', 'error')
			return redirect(url_for('quiz.quiz_browse_page'))
		if (quiz.details.current_players >= quiz.parent_pricing_plan.total_players):
			flash('No slots left for new players. Try registering for some other quiz.', 'error')
			return redirect(url_for('quiz.quiz_browse_page'))
		if subscriber_exists_in_quiz(current_user, quiz):
			flash('You seem to have already registered for this quiz', 'info')
			return redirect(url_for('quiz.quiz_browse_page'))
		if quiz.quiz_master.user_id == current_user.id:
			flash('You may not register for quizzes that you are hosting.', 'error')
			return redirect(url_for('quiz.quiz_browse_page'))

		new_subscriber = create_quiz_subscriber(current_user, quiz)
		if not new_subscriber:
			flash('Something went wrong while subscribing you to the quiz. Try reporting to the developers.')
			return redirect(url_for('quiz.quiz_register_page'))

		return redirect(url_for('quiz.quiz_register_payment_page', uuid=quiz.id))
	return render_template('quiz/quiz_register.html', quiz=quiz)

@quiz.route('/quiz/register/pay/<string:uuid>', methods=['GET', 'POST'])
@login_required
@profile_required
def quiz_register_payment_page(uuid):
	quiz = get_quiz_for_uuid(uuid)
	quiz_owner = quiz.quiz_owner
	if current_user == quiz_owner:
		flash('You may not register for quizzes you already own.')
		return redirect(url_for('quiz.quiz_browse_page'))

	if not subscriber_exists_in_quiz(current_user, quiz):
		flash('You are not subscribed to this quiz. Please subscribe first.', 'error')
		return redirect(url_for('quiz.quiz_register_page',uuid=uuid))

	subscriber = get_subscriber_for_user_id(current_user, quiz)
	print('pop=',subscriber.payment_status)
	if subscriber.payment_status:
		flash('You have already paid for this quiz! :)', 'success')
		return redirect(url_for('user_dashboard.user_dashboard_page'))

	razorpay_order = RazorpayOrder(
						order_amount=(quiz.details.subscription_price*100),
						order_receipt="Registering for Quiz "+quiz.details.name,
						order_client_name=current_user.profile.first_name+" "+current_user.profile.last_name,
						order_client_email=current_user.email,
						order_client_phone=current_user.profile.phone_number,
						order_pricing_plan_name="Host: "+quiz.quiz_owner.parent_user.profile.first_name+" "+quiz.quiz_owner.parent_user.profile.last_name,
						quiz_uuid=quiz.id
						)
	razorpay_options = razorpay_order.get_razorpay_order_options()
	return render_template('quiz/quiz_register_payment_page.html', quiz=quiz, razorpay_options=dict(razorpay_options))

@quiz.route("/quiz/create/pay/<string:uuid>")
@login_required
def quiz_create_payment_page(uuid):
	quiz = get_quiz_for_uuid(uuid)
	quiz_owner = quiz.quiz_owner
	if not (quiz_owner.user_id == current_user.id):
		flash('You may not pay for quizzes you do not own.')
		return redirect(url_for('user_dashboard.user_dashboard_page'))
	razorpay_order = RazorpayOrder(
								order_amount=(quiz.parent_pricing_plan.price*100),
								order_receipt=quiz.parent_pricing_plan.name,
								order_client_name=current_user.profile.first_name + current_user.profile.last_name,
								order_client_email=current_user.email,
								order_client_phone=current_user.profile.phone_number,
								order_pricing_plan_name=quiz.parent_pricing_plan.name,
								quiz_uuid=quiz.id
								)

	razorpay_options = razorpay_order.get_razorpay_order_options()
	return render_template('quiz/quiz_create_payment_page.html', quiz=quiz, razorpay_options=dict(razorpay_options))

@quiz.route('/quiz/register/pay/callback/<string:uuid>', methods=['POST'])
@csrf_protect.exempt
@login_required
def quiz_register_payment_callback_url(uuid):
	razorpay_payment_id = request.form.get('razorpay_payment_id', '')
	razorpay_order_id = request.form.get('razorpay_order_id', '')
	razorpay_signature = request.form.get('razorpay_signature', '')
	params_dict = {
	'razorpay_payment_id': razorpay_payment_id,
	'razorpay_order_id': razorpay_order_id,
	'razorpay_signature': razorpay_signature
	}
	quiz = get_quiz_for_uuid(uuid)
	subscriber = get_subscriber_for_user_id(current_user, quiz)
	amount = quiz.details.subscription_price
	payment_state = razorpay_verify_payment_signature(params_dict, amount)
	if not payment_state:
		abort(404, description='This is fatal. The payment signature was not verified. Please report to the developers.')

	sub = add_quiz_subscriber_payment_details(current_user, quiz, params_dict)
	if not sub:
		flash('Had problems adding your details to the database.', 'error')
		return redirect(url_for('user_dashboard.user_dashboard_page'))
	
	return redirect(url_for('user_dashboard.user_quiz_subscribed_receipt', uuid=quiz.id))

@csrf_protect.exempt
@quiz.route("/quiz/create/pay/callback/<string:uuid>", methods=['POST'])
@login_required
def quiz_create_payment_callback_url(uuid):
	params_dict = {
	'razorpay_payment_id': request.form.get('razorpay_payment_id', ''),
	'razorpay_order_id': request.form.get('razorpay_order_id', ''),
	'razorpay_signature': request.form.get('razorpay_signature', '')
	}
	quiz = Quiz.query.filter(Quiz.id == uuid).first()
	if not quiz:
		abort(404, description='Something went wrong. The quiz UUID wasnt found.')
	amount = quiz.parent_pricing_plan.price
	payment_state = razorpay_verify_payment_signature(params_dict, amount)
	if not payment_state:
		abort(404, description='This is fatal. The payment signature was not verified. Please report to the developers.')

	add_quiz_owner_payment_details(quiz.quiz_owner.id, quiz.parent_pricing_plan.price, params_dict)
	return redirect(url_for('user_dashboard.user_quiz_owned_receipt', uuid=quiz.id))

@csrf_protect.exempt
@quiz.route('/quiz/register/refund', methods=['POST'])
@login_required
def quiz_register_refund():
	request_data = request.get_json()
	subscriber_id = request_data['subscriber_id']
	quiz_uuid = request_data['quiz_uuid']
	subscriber = QuizSubscriber.query.filter(QuizSubscriber.user_id == subscriber_id).first()
	quiz = Quiz.query.filter(Quiz.uuid == quiz_uuid).first()

	if not subscriber in quiz.subscribers:
		abort(404, description="You are not a subscriber to this quiz, hence you may not rescind the participation.")

	if not subscriber.payment_status:
		response = {
		"status": "OK",
		"payment_status": False,
		"payment_message": "You did not pay for the quiz, hence you shall recieve no refund.",
		"participation_message": "Your participation has been successfully rescinded."
		}
		# Delete subscription here
		return json.dumps(response)

	response = {
	"status": "OK",
	"payment_status": True,
	"payment_message": "We have issued an refund of ₹ "+str(subscriber.payment_amount)+" to your source of debit. You should recieve it within 5 - 7 working days. Feel free to contact us on Discord for any queries.",
	"participation_message": "Your participation has been successfully rescinded."
	}
	
	return json.dumps(response)
