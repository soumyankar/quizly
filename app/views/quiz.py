import uuid
import json
from datetime import datetime, date
from app import db, csrf_protect
from app.forms.quizforms import QuizRegisterForm
from app.misc.razorpay_creds import RazorpayOrder, razorpay_verify_payment_signature
from app.models.models import PricingPlan, Quiz, User, QuizOwner, QuizMaster, QuizSubscriber, UserProfile
from flask import (Blueprint, Flask, flash, redirect, render_template, request,url_for,abort)
from flask_login import current_user, login_required
from flask_sqlalchemy import SQLAlchemy

quiz = Blueprint("quiz", __name__, static_folder="static", template_folder="templates")

@quiz.route("/quiz/", methods=['GET', 'POST'])
def quiz_homepage():
	return render_template('quiz/quiz.html')

@quiz.route("/quiz/create/<int:plan>", methods=['GET', 'POST'])
@login_required
def quiz_create_page(plan):
	user_profile = UserProfile.query.filter(UserProfile.user_id == current_user.id).first()
	if not user_profile or user_profile.profile_complete == False:
		flash('Please <a href="'+url_for('user.edit_user_profile')+'">complete your profile</a> otherwise you may not be allowed to <b>Create a Quiz</b> or <b>Subscribe to a Quiz</b>.', 'error')
		return redirect(request.referrer)

	chosen_plan = PricingPlan.query.filter(PricingPlan.id == plan).first()
	if not chosen_plan:
		flash('That is not a valid plan ID. Choose again')
		return redirect(url_for('quiz.quizplanspage'))
	form = QuizRegisterForm()
	form.quiz_master.choices = [(user.id, user.email) for user in User.query.all()]
	if request.method == 'POST':
		if form.validate_on_submit():
			while True:
				new_uuid = str(uuid.uuid4())
				if not (Quiz.query.filter(Quiz.uuid == new_uuid).first()):
					break
			new_quiz = Quiz(
				uuid = new_uuid,
				name = form.name.data,
				date = form.date.data,
				time = form.time.data,
				active = False,
				current_players = 0,
				subscription_price = form.subscription_price.data,
				total_players = chosen_plan.total_players
				)
			new_quiz_owner = QuizOwner()
			new_quiz_owner.parent_quiz = new_quiz
			new_quiz_owner.parent_user = current_user
			new_quiz_owner.parent_pricing_plan = chosen_plan
			new_quiz_owner.payment_amount = chosen_plan.price
			new_quiz_master = QuizMaster()
			new_quiz_master.parent_quiz = new_quiz
			new_quiz_master.parent_user = current_user
			db.session.add(new_quiz)
			db.session.add(new_quiz_owner)
			db.session.add(new_quiz_master)
			db.session.commit()
			if new_quiz.quiz_owner.parent_pricing_plan.payment_required == False:
				new_quiz_owner.payment_status = True
				new_quiz_owner.payment_date = date.today()
				new_quiz_owner.payment_time = datetime.now().time()
				new_quiz_owner.razorpay_payment_id = 'free_quiz'
				new_quiz_owner.razorpay_order_id = 'free_quiz'
				new_quiz_owner.razorpay_signature = 'free_quiz'
				db.session.commit()
				return render_template('razorpay/payment_invoice.html', payment_state=True, description="Quiz Creation fee for Quiz UUID: "+new_quiz.uuid , client=new_quiz_owner, uuid=new_quiz.uuid, params_dict = {'razorpay_payment_id': 'free_quiz' } )
			return redirect(url_for('quiz.quiz_create_payment_page', uuid=new_uuid))
	return render_template('quiz/quiz_create.html', chosen_plan=chosen_plan, form=form)

@quiz.route("/quiz/browse", methods=['GET', 'POST'])
def quiz_browse_page():
	quizzes = Quiz.query.all()
	return render_template('quiz/quiz_browse.html', quizzes=quizzes)

@csrf_protect.exempt
@quiz.route("/quiz/register/<string:uuid>", methods=['GET', 'POST'])
@login_required
def quiz_register_page(uuid):
	user_profile = UserProfile.query.filter(UserProfile.user_id == current_user.id).first()
	if not user_profile or user_profile.profile_complete == False:
		flash('Please <a href="'+url_for('user.edit_user_profile')+'">complete your profile</a> otherwise you may not be allowed to <b>Create a Quiz</b> or <b>Subscribe to a Quiz</b>.', 'error')
		return redirect(request.referrer)
	
	quiz = Quiz.query.filter(Quiz.uuid == uuid).first()
	if request.method == 'POST':
		quiz_owner = quiz.quiz_owner
		if not quiz_owner:
			flash('This quiz does not have a quiz owner. Registration may not be allowed')
			return redirect(request.referrer)
		if (quiz_owner.user_id == current_user.id):
			flash('You may not register for quizzes you already own.')
			return redirect(url_for('quiz.quiz_browse_page'))
		if (quiz.current_players >= quiz.total_players):
			flash('No slots left for new players. Try registering for some other quiz.')
			return redirect(url_for('quiz.quiz_register_page', uuid=quiz.uuid))
		new_subscriber = QuizSubscriber(
			user_confirm=True,
			payment_amount=quiz.subscription_price,
			payment_status=False
			)
		new_subscriber.parent_quiz=quiz
		new_subscriber.parent_user=current_user
		quiz.subscribers.append(new_subscriber)
		db.session.add(new_subscriber)
		db.session.add(quiz)
		db.session.commit()
		return redirect(url_for('quiz.quiz_register_payment_page', uuid=quiz.uuid))
	return render_template('quiz/quiz_register.html', quiz=quiz)

@quiz.route("/quiz/plans", methods=['GET', 'POST'])
def quiz_plans_page():
	pricing_plans = PricingPlan.query.all()
	return render_template('quiz/quiz_plans.html', pricing_plans=pricing_plans)

@quiz.route('/quiz/register/pay/<string:uuid>', methods=['GET', 'POST'])
@login_required
def quiz_register_payment_page(uuid):
	quiz = Quiz.query.filter(Quiz.uuid == uuid).first()
	quiz_owner = quiz.quiz_owner
	if (quiz_owner.user_id == current_user.id):
		flash('You may not register for quizzes you already own.')
		return redirect(url_for('quiz.quiz_browse_page'))

	subscriber_exists = False
	for subscriber in quiz.subscribers:
		if subscriber.user_id == user.id:
			subscriber_exists = True
			break

	if subscriber_exists == False:
		flash('You are not subscribed to this quiz. Please subscribe first.', 'error')
		return redirect(request.referrer)

	razorpay_order = RazorpayOrder(
						order_amount=(quiz.subscription_price*100),
						order_receipt="Registering for Quiz "+quiz.name,
						order_client_name="fix this later",
						order_client_email="fixthislater@gmail.com",
						order_pricing_plan_name="(fix) Host = " + quiz.quiz_owner.parent_user.username,
						quiz_uuid=quiz.uuid
						)
	razorpay_options = razorpay_order.get_razorpay_order_options()
	return render_template('quiz/quiz_register_payment_page.html', quiz=quiz, razorpay_options=dict(razorpay_options))

@quiz.route("/quiz/create/pay/<string:uuid>")
@login_required
def quiz_create_payment_page(uuid):
	quiz = Quiz.query.filter(Quiz.uuid == uuid).first()
	quiz_owner = quiz.quiz_owner
	if not (quiz_owner.user_id == current_user.id):
		flash('You may not pay for quizzes you do not own.')
		return redirect(url_for('user_dashboard.user_dashboard_page'))
	razorpay_order = RazorpayOrder(
								order_amount=(quiz_owner.payment_amount*100),
								order_receipt=quiz_owner.parent_pricing_plan.name,
								order_client_name="fix this later",
								order_client_email="fixthislater@gmail.com",
								order_pricing_plan_name=quiz_owner.parent_pricing_plan.name,
								quiz_uuid=quiz.uuid
								)

	razorpay_options = razorpay_order.get_razorpay_order_options()
	return render_template('quiz/quiz_create_payment_page.html', quiz=quiz, razorpay_options=dict(razorpay_options))

@csrf_protect.exempt
@quiz.route('/quiz/register/pay/callback/<string:uuid>', methods=['POST'])
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
	quiz = Quiz.query.filter(Quiz.uuid == uuid).first()
	subscriber = QuizSubscriber.query.filter(QuizSubscriber.user_id == current_user.id).first()
	amount = quiz.subscription_price
	payment_state = razorpay_verify_payment_signature(params_dict, amount)
	description = "Registration Fee for Quiz UUID: "+quiz.uuid
	if payment_state == True:
		subscriber.payment_status = True
		subscriber.payment_date = date.today()
		subscriber.payment_time = datetime.now().time()
		subscriber.razorpay_payment_id = razorpay_payment_id
		subscriber.razorpay_order_id = razorpay_order_id
		subscriber.razorpay_signature = razorpay_signature
		quiz.current_players = quiz.current_players + 1
		db.session.commit()
	
	return render_template('razorpay/payment_invoice.html', payment_state=payment_state, description=description , client=subscriber, uuid=uuid, params_dict=params_dict)


@csrf_protect.exempt
@quiz.route("/quiz/create/pay/callback/<string:uuid>", methods=['POST'])
@login_required
def quiz_create_payment_callback_url(uuid):
	razorpay_payment_id = request.form.get('razorpay_payment_id', '')
	razorpay_order_id = request.form.get('razorpay_order_id', '')
	razorpay_signature = request.form.get('razorpay_signature', '')
	params_dict = {
	'razorpay_payment_id': razorpay_payment_id,
	'razorpay_order_id': razorpay_order_id,
	'razorpay_signature': razorpay_signature
	}
	quiz = Quiz.query.filter(Quiz.uuid == uuid).first()
	amount = quiz.quiz_owner.payment_amount
	payment_state = razorpay_verify_payment_signature(params_dict, amount)
	owner = quiz.quiz_owner
	description = "Quiz Creation Fee for Quiz UUID: "+quiz.uuid
	if payment_state == True:
		owner.payment_status = True
		owner.payment_date = date.today()
		owner.payment_time = datetime.now().time()
		owner.razorpay_payment_id = razorpay_payment_id
		owner.razorpay_order_id = razorpay_order_id
		owner.razorpay_signature = razorpay_signature
		db.session.commit()

	return render_template('razorpay/payment_invoice.html', payment_state=payment_state, description=description , client=owner, uuid=uuid, params_dict=params_dict)

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
