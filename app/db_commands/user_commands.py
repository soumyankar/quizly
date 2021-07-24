from app import db
from datetime import datetime, date
from app.misc.razorpay_creds import RazorpayOrder, razorpay_verify_payment_signature
from app.models.models import PricingPlan, Quiz, User, QuizOwner, QuizMaster, QuizSubscriber, UserProfile

def append_owned_quiz_to_user(quiz, user):
	user.quizzes_owned.append(quiz)
	db.session.commit()

def get_user_profile(user_id):
	user_profile = UserProfile.query.filter(UserProfile.user_id == user_id).first()
	return user_profile

def get_quiz_for_uuid(uuid):
	quiz = Quiz.query.filter(Quiz.id == uuid).first()
	return quiz

def get_quiz_master_choices_for_uuid(uuid):
	quiz = Quiz.query.filter(Quiz.id == uuid).first()
	if not quiz:
		return False
	quiz_subscribers = quiz.subscribers
	choices = []
	for user in User.query.all():
		if user.profile and user.profile.profile_complete:
			if not user in quiz_subscribers:
				choice_label = user.profile.first_name + " " + user.profile.last_name +" ("+user.email+")"
				choices.append( (user.id, choice_label) )

	return choices

def get_subscriber_for_user_id(user, quiz):
	subscriber = QuizSubscriber.query.filter(QuizSubscriber.user_id == user.id and QuizSubscriber.quiz_id == quiz.id).first()
	return subscriber

def get_browse_quizzes():
	browse_quizzes = []
	all_quizzes = Quiz.query.all()
	for quiz in all_quizzes:
		if not quiz.quiz_master or not quiz.quiz_owner or not quiz.details:
			continue
		browse_quizzes.append(quiz)
	return browse_quizzes

def subscriber_exists_in_quiz(user, quiz):
	for subscriber in quiz.subscribers:
		if subscriber.user_id == user.id:
			return True
	return False

def master_exists_in_quiz(user, quiz):
	if quiz:
		if quiz.quiz_master:
			if quiz.quiz_master.user_id == user.id:
				return True
	return False

def get_quiz_master_for_user_id(user, quiz):
	quiz_master = QuizMaster.query.filter(QuizMaster.user_id == user.id and QuizMaster.quiz_id == quiz.id).first()
	if not quiz_master:
		return None
	return quiz_master