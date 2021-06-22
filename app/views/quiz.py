from flask import Flask, request, redirect, url_for, Blueprint, render_template, flash
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy
import uuid

from app import db
from app.models.models import User, Quiz, PricingPlan
from app.forms.quizforms import QuizRegisterForm
from app.misc.razorpay_creds import razorpay_client, RazorpayOrder

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

@quiz.route("/quiz/browse", methods=['GET', 'POST'])
def quizbrowsepage():
	quizzes = Quiz.query.all()
	owner_names = []
	pricing_plans = []
	for quiz in quizzes:
		user = User.query.filter(User.id == quiz.id).first()
		owner_names.append(str(user.first_name + user.last_name))
		plan = PricingPlan.query.filter(PricingPlan.id == quiz.pricingplan).first()
		pricing_plans.append(plan.name)
	return render_template('quiz/quizbrowse.html', quizzes=quizzes, owner_names=owner_names, pricing_plans=pricing_plans)

@quiz.route("/quiz/register/<string:uuid>", methods=['GET', 'POST'])
@login_required
def quizregisterpage(uuid):
	quiz = Quiz.query.filter(Quiz.uuid == uuid).first()
	owner = User.query.filter(User.id == quiz.id).first()
	pricing_plan = PricingPlan.query.filter(PricingPlan.id == quiz.pricingplan).first()

	return render_template('quiz/quizregister.html', quiz=quiz, owner=owner, pricing_plan=pricing_plan)
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

	razorpay_order = RazorpayOrder(order_amount=(pricing_plan_used.price*100),
								order_receipt=pricing_plan_used.name,
								order_client_name=current_user.first_name,
								order_client_email=current_user.email,
								order_pricing_plan_name=pricing_plan_used.name)

	razorpay_options = razorpay_order.get_razorpay_order_options()

	return render_template('quiz/quizpayment.html', quiz=quiz, pricing_plan_used=pricing_plan_used, razorpay_options=razorpay_options)

