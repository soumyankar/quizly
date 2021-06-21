from app import db
from datetime import datetime

class PricingPlan(db.Model):
	__tablename__ = 'pricingplans'
	id = db.Column(db.Integer(), primary_key=True)

	name = db.Column(db.String(50), nullable=False, server_default=u'unknown')
	price = db.Column(db.Integer(), nullable=False, default=0)
	payment_required = db.Column(db.Boolean, nullable=False, default=False)
	popular_plan = db.Column(db.Boolean, nullable=False, default=False)
	total_players = db.Column(db.Integer(), nullable=False, default=20)
	active = db.Column(db.Boolean, nullable=False, default=True)