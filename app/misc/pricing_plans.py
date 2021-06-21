class BasicPricingPlan():
	order_amount = 0
	order_currency = 'INR'
	order_receipt = 'This is the order receipt'
	notes = {
		'Plan': 'Basic Pricing Plan',
		'Players': '0-19',
		'Hosted on': 'Discord'
		}   # OPTIONAL

class PremiumPricingPlan():
	order_amount = 150
	order_currency = 'INR'
	order_receipt = 'This is the order receipt'
	notes = {
		'Plan': 'Premium Pricing Plan',
		'Players': '0-99',
		'Hosted on': 'Discord'
		}   # OPTIONAL