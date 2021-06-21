from app import db
from datetime import datetime

class PricingPlan(db.model):
	__tablename__ = 'pricingplans'
	id = db.Column(db.Integer, primary_key=true)

	name = db.Column(db.String(50), nullable=False)
	price = db.Column(db.Integer, nullable=False)
	payment_required = db.Column(db.Boolean, nullable=False)
	total_players = db.Column(db.Integer, nullable=False)