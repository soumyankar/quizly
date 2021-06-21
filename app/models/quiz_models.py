from app import db
from datetime import datetime
from .user_models import User

class Quiz(db.Model):
	__tablename__ = 'quiz'
	id = db.Column(db.Integer(), primary_key=True)

	uuid = db.Column(db.String(255), nullable=False)
	name = db.Column(db.String(50), nullable=False)
	date = db.Column(db.DateTime, nullable=False)
	time = db.Column(db.DateTime, nullable=False)
	current_players = db.Column(db.Integer(), nullable=True, default=0)
	total_players = db.Column(db.Integer(), nullable=False)

	payment_status = db.Column(db.Boolean, default=False)
	# Relationships
	# One to one relationship to ownner
	owner = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
	# Many to many relationship to subscriber
	subscribers = db.Column('User', secondary='quiz_subscribers', 
							backref=db.backref('quiz', lazy='dynamic'))

class QuizSubscriptions(db.Model):
	__tablename__ = 'quiz_subscriptions'

	id = db.Column(db.Integer(), primary_key=True)
	user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
	quiz_id = db.Column(db.Integer(), db.ForeignKey('quiz.id', ondelete='CASCADE'))

class QuizSubscribers(db.Model):
	__tablename__ = 'quiz_subscribers'	
	user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
	quiz_id = db.Column(db.Integer(), db.ForeignKey('quiz.id', ondelete='CASCADE'))