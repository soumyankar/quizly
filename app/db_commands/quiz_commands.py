from app import db
from datetime import datetime, date
from app.misc.razorpay_creds import RazorpayOrder, razorpay_verify_payment_signature
from app.models.models import *
from app.db_commands.user_commands import *

def create_quiz(plan, owner):
	new_quiz = Quiz()
	new_quiz.parent_pricing_plan = plan
	new_quiz_owner = QuizOwner()
	new_quiz_owner.parent_user = owner
	new_quiz_owner.parent_quiz = new_quiz
	new_quiz.quiz_owner = new_quiz_owner

	append_owned_quiz_to_user(new_quiz_owner, owner)
	db.session.add(new_quiz)
	db.session.add(new_quiz_owner)
	db.session.commit()
	return new_quiz

def add_quiz_owner_payment_details(quiz_owner_id, payment_amount, razorpay_payment_keys):

	quiz_owner = QuizOwner.query.filter(QuizOwner.id == quiz_owner_id).first()
	if not quiz_owner:
		return False
	quiz_owner.payment_date = date.today()
	quiz_owner.payment_time = datetime.now().time()
	quiz_owner.payment_amount = payment_amount
	quiz_owner.razorpay_payment_id = razorpay_payment_keys['razorpay_payment_id']
	quiz_owner.razorpay_order_id = razorpay_payment_keys['razorpay_order_id']
	quiz_owner.razorpay_signature = razorpay_payment_keys['razorpay_signature']
	quiz_owner.payment_status = True
	db.session.add(quiz_owner)
	db.session.commit()
	return quiz_owner

def create_quiz_master(user, quiz):
	new_quiz_master = quiz.quiz_master
	if not new_quiz_master:
		new_quiz_master = QuizMaster(user_confirm = False)

	new_quiz_master.parent_user = user
	new_quiz_master.parent_quiz = quiz
	user.quizzes_hosted.append(new_quiz_master)
	quiz.quiz_master = new_quiz_master
	db.session.add(new_quiz_master)
	db.session.commit()

	return new_quiz_master

def create_quiz_details(form, user, uuid):

	quiz=Quiz.query.filter(Quiz.id == uuid).first()
	if not quiz:
		return False
	new_quiz_details = QuizDetails(
		name = form.name.data,
		date = form.date.data,
		time = form.time.data,
		current_players = 0,
		subscription_price = form.subscription_price.data)
	new_quiz_details.parent_quiz = quiz
	quiz.details = new_quiz_details
	quiz.quiz_master = create_quiz_master(user, quiz)
	db.session.add(new_quiz_details)
	db.session.add(quiz)
	db.session.commit()

	return new_quiz_details

def create_quiz_subscriber(user, quiz):
	new_subscriber = QuizSubscriber(
	user_confirm=True,
	payment_amount=quiz.details.subscription_price,
	payment_status=False
	)
	new_subscriber.parent_quiz=quiz
	new_subscriber.parent_user=user
	quiz.subscribers.append(new_subscriber)
	user.subscriptions.append(new_subscriber)
	db.session.add(new_subscriber)
	db.session.add(quiz)
	db.session.commit()

	return new_subscriber

def add_quiz_subscriber_payment_details(user, quiz, razorpay_payment_keys):
	subscriber = QuizSubscriber.query.filter(QuizSubscriber.user_id == user.id).first()
	if not subscriber:
		create_quiz_subscriber(user,quiz)

	subscriber.payment_status = True
	subscriber.payment_date = date.today()
	subscriber.payment_time = datetime.now().time()
	subscriber.razorpay_payment_id = razorpay_payment_keys['razorpay_payment_id']
	subscriber.razorpay_order_id = razorpay_payment_keys['razorpay_order_id']
	subscriber.razorpay_signature = razorpay_payment_keys['razorpay_signature']
	quiz.details.current_players = quiz.details.current_players + 1
	db.session.add(subscriber)
	db.session.commit()
	return subscriber