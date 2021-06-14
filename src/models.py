from flask_login import UserMixin
from .extensions import db
from datetime import datetime

class Admin(UserMixin, db.Model):
	id=db.Column(db.Integer, primary_key=True)
	username=db.Column(db.String(15),unique=True)
	email=db.Column(db.String(80),unique=True)
	password=db.Column(db.String(80))
	date_created=db.Column(db.DateTime, default=datetime.now())
	
	def __repr__(self):
		return '<Admin %r>' % self.id
