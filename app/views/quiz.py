import uuid

from app import db, csrf_protect
from app.forms.quizforms import QuizRegisterForm
from app.misc.razorpay_creds import RazorpayOrder, razorpay_verify_payment_signature
from app.models.models import PricingPlan, Quiz, User, QuizOwner, QuizPayment, QuizMaster, QuizSubscriber
from flask import (Blueprint, Flask, flash, redirect, render_template, request,url_for)
from flask_login import current_user, login_required
from flask_sqlalchemy import SQLAlchemy

quiz = Blueprint("quiz", __name__, static_folder="static", template_folder="templates")

@quiz.route("/quiz/", methods=['GET', 'POST'])
def quizhomepage():
	return render_template('quiz/quiz.html')

@quiz.route("/quiz/create/<int:plan>", methods=['GET', 'POST'])
@login_required
def quizcreatepage(plan):
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
				current_players = 0,
				subscription_price = form.subscription_price.data,
				total_players = chosen_plan.total_players
				)

			new_quiz_owner = QuizOwner()
			new_quiz_owner.parent_quiz = new_quiz
			new_quiz_owner.parent_user = current_user
			new_quiz_master = QuizMaster()
			new_quiz_master.parent_quiz = new_quiz
			new_quiz_master.parent_user = current_user
			new_quiz_payment = QuizPayment()
			new_quiz_payment.parent_pricing_plan = chosen_plan
			new_quiz_payment.parent_quiz = new_quiz

			db.session.add(new_quiz)
			db.session.add(new_quiz_owner)
			db.session.add(new_quiz_master)
			db.session.add(new_quiz_payment)
			db.session.commit()
			return redirect(url_for('quiz.quizpaymentpage', uuid=new_uuid))
	return render_template('quiz/quizcreate.html', chosen_plan=chosen_plan, form=form)

@quiz.route("/quiz/browse", methods=['GET', 'POST'])
def quiz_browse_page():
	quizzes = Quiz.query.all()
	return render_template('quiz/quiz_browse.html', quizzes=quizzes)

@csrf_protect.exempt
@quiz.route("/quiz/register/<string:uuid>", methods=['GET', 'POST'])
@login_required
def quiz_register_page(uuid):
	quiz = Quiz.query.filter(Quiz.uuid == uuid).first()
	if request.method == 'POST':
		quiz_owner = quiz.quiz_owner.parent_user.id
		if (quiz_owner == current_user.id):
			flash('You may not register for quizzes you already own.')
			return redirect(url_for('quiz.quiz_browse_page'))
		new_subscriber = QuizSubscriber(
			user_confirm=False,
			subscription_price=quiz.quiz_payment.parent_pricing_plan.price,
			payment_status=False
			)
		new_subscriber.parent_quiz=quiz
		new_subscriber.parent_user=current_user
		db.session.add(new_subscriber)
		db.session.commit()
		return redirect(url_for('quiz.quiz_register_payment_page', uuid=quiz.uuid))
	return render_template('quiz/quiz_register.html', quiz=quiz)

@quiz.route('/quiz/register/pay/<string:uuid>', methods=['GET', 'POST'])
@login_required
def quiz_register_payment_page(uuid):
	quiz = Quiz.query.filter(Quiz.uuid == uuid).first()
	quiz_owner = quiz.quiz_owner.parent_user.id
	if (quiz_owner == current_user.id):
		flash('You may not register for quizzes you already own.')
		return redirect(url_for('quiz.quiz_browse_page'))
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

@quiz.route("/quiz/plans", methods=['GET', 'POST'])
def quizplanspage():
	pricingplans = PricingPlan.query.all()
	return render_template('quiz/quizplans.html', pricingplans=pricingplans)

@quiz.route("/quiz/create/pay/<string:uuid>")
@login_required
def quizpaymentpage(uuid):
	quiz = Quiz.query.filter(Quiz.uuid == uuid).first()
	quiz_owner = quiz.quiz_owner.parent_user.id
	if not (quiz_owner == current_user.id):
		flash('You may not pay for quizzes you do not own.')
		return redirect(url_for(userdashboard.userdashboardpage))
	pricing_plan_used = PricingPlan.query.filter(PricingPlan.id == quiz.pricingplan).first()

	pricing_plan_used_id = quiz.quiz_payment.pricing_plan_id
	pricing_plan_used = PricingPlan.query.filter(PricingPlan.id == pricing_plan_used_id).first()
	razorpay_order = RazorpayOrder(
								order_amount=(pricing_plan_used.price*100),
								order_receipt=pricing_plan_used.name,
								order_client_name="fix this later",
								order_client_email="fixthislater@gmail.com",
								order_pricing_plan_name=pricing_plan_used.name,
								quiz_uuid=quiz.uuid
								)

	razorpay_options = razorpay_order.get_razorpay_order_options()
	return render_template('quiz/quizpayment.html', quiz=quiz, pricing_plan_used=pricing_plan_used, razorpay_options=dict(razorpay_options))

@csrf_protect.exempt
@quiz.route('/quiz/register/pay/callback/<string:uuid>', methods=['POST'])
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
	if payment_state == True:
		subscriber.payment_status = True
		db.session.commit()
		return redirect(url_for('quiz.quiz_payment_callback_success', uuid=uuid))
	if payment_state == False:
		return redirect(url_for('quiz.quiz_payment_callback_failure', uuid=uuid))

@csrf_protect.exempt
@quiz.route("/quiz/create/pay/callback/<string:uuid>", methods=['POST'])
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
	amount = quiz.quiz_payment.parent_pricing_plan.price
	payment_state = razorpay_verify_payment_signature(params_dict, amount)
	if payment_state == True:
		quiz.quiz_payment.payment_status = True
		db.session.commit()
		return redirect(url_for('quiz.quiz_payment_callback_success', uuid=uuid))
	if payment_state == False:
		return redirect(url_for('quiz.quiz_payment_callback_failure', uuid=uuid))

@quiz.route('/quiz/pay/success/<string:uuid>', methods=['GET'])
def quiz_payment_callback_success(uuid):
	return render_template('quiz/quiz_payment_callback_success.html')

@quiz.route('/quiz/pay/failure/<string:uuid>', methods=['GET'])
def quiz_payment_callback_failure(uuid):
	return render_template('quiz/quiz_payment_callback_failure.html')