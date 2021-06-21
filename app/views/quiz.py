from flask import Flask, request, redirect, url_for, Blueprint, render_template, flash
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy
import uuid

from app import db
from app.models.models import Quiz, PricingPlan
from app.forms.quizforms import QuizRegisterForm
from app import razorpay_client
from app.local_settings import RAZORPAY_KEY_SECRET, RAZORPAY_KEY_ID

quiz = Blueprint("quiz", __name__, static_folder="static", template_folder="templates")

@quiz.route("/quiz/", methods=['GET', 'POST'])
def quizhomepage():
	return render_template('quiz/quiz.html')

@quiz.route("/quiz/plans/create/<int:plan>", methods=['GET', 'POST'])
@login_required
def quizcreatepage(plan):
	try:
		chosen_plan = PricingPlan.query.filter(PricingPlan.id == plan).first()
		form = QuizRegisterForm()
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
					total_players = chosen_plan.total_players,
					payment_status = False,
					owner = current_user.id,
					pricingplan = plan
					)
				db.session.add(new_quiz)
				db.session.commit()

				return redirect(url_for('quiz.quizpaymentpage', uuid=new_uuid))
		return render_template('quiz/quizcreate.html', chosen_plan=chosen_plan, form=form)
	except:
		flash('That is not a valid plan ID. Choose again')
		return redirect(url_for('quiz.quizplanspage'))

@quiz.route("/quiz/register", methods=['GET', 'POST'])
def quizregisterPage():
	return render_template('quiz/quizregister.html')

@quiz.route("/quiz/plans", methods=['GET', 'POST'])
def quizplanspage():
	pricingplans = PricingPlan.query.all()
	return render_template('quiz/quizplans.html', pricingplans=pricingplans)

@quiz.route("/quiz/plans/pay/<string:uuid>")
@login_required
def quizpaymentpage(uuid):
	quiz = Quiz.query.filter(Quiz.uuid == uuid).first()
	if not (quiz.owner == current_user.id):
		flash('You may not pay for quizzes you do not own.')
		return redirect(url_for(userdashboard.userdashboardpage))
	pricing_plan_used = PricingPlan.query.filter(PricingPlan.id == quiz.pricingplan).first()

	order_amount = pricing_plan_used.price
	order_currency = 'INR'
	order_receipt = 'This is the receipt. IDK.'
	notes = {'SOme note': 'This is a note'}   # OPTIONAL
	client_order = dict(amount=order_amount, currency=order_currency, receipt=order_receipt, notes=notes)
	print(client_order)
	order_id = razorpay_client.order.create(client_order)
	order_id = order_id.get('id')
	print (order_id)
	razorpay_key = RAZORPAY_KEY_ID
	return render_template('quiz/quizpayment.html', quiz=quiz, pricing_plan_used=pricing_plan_used, order_id=order_id, razorpay_key=razorpay_key)