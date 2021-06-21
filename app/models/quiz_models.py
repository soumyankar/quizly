from app import db
from datetime import datetime

class Quiz(db.model):
	__tablename__ = 'quiz'
	id = db.Column(db.Integer, primary_key=true)

	uuid = db.Column(db.String(50), nullable=False)
	name = db.Column(db.String(50), nullable=False)
	date = db.Column(db.DateTime, nullable=False)
	time = db.Column(db.DateTime, nullable=False)
	current_players = db.Column(db.Integer, nullable=True, default=0)
	total_players = db.Column(db.Integer, nullable=False)

	payment_status = db.Column(db.Boolean, default=False)

class QuizRole(db.model):
	__tablename__ = 'quizroles'

	id = db.Column(db.Integer, primary_key=true)
	name = db.Column(db.String(50), nullable=False, server_default=u'', unique=True)
	label = db.Column(db.Unicode(255), server_default=u'')  # for display purposes

class QuizPlayerRoles(db.model):
	__tablename__ = 'quizplayerroles'

	id = db.Column(db.Integer, primary_key=true)
	user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
	role_id = db.Column(db.Integer(), db.ForeignKey('quizroles.id', ondelete='CASCADE'))
