import razorpay
from app.local_settings import RAZORPAY_KEY_SECRET, RAZORPAY_KEY_ID
from app.settings import APP_NAME
import json
# Razorpay
razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

options ={
    "key": "", # Enter the Key ID generated from the Dashboard
    "amount": "", # Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
    "currency": "INR", # INR Probably.
    "name": "", # org name
    "description": "", # pricing plan here maybe
    "image": "https://example.com/your_logo", # Need to put in logo here.
    "order_id": "", #This is a sample Order ID. Pass the `id` obtained in the response of Step 1
    "callback_url": "https://eneqd3r9zrjok.x.pipedream.net/", # this will be the callback url for us.
    "prefill": {
        "name": "",
        "email": ""
    }, # Client details here.
    "notes": {
        "address": "GetSetQuiz Office" # Unsue how the receipt would look like so unsure what to put here.
    },
    "theme": {
        "color": "#3399cc" # rishabh0282 will handle this.
    }
}

class RazorpayOrder():

	def __init__(self, order_amount, order_receipt, order_client_name, order_client_email, order_pricing_plan_name):
		self.new_order_id = ""
		self.new_order_amount = order_amount
		self.new_order_receipt = order_receipt
		self.new_order_client_name = order_client_name
		self.new_order_client_email = order_client_email
		self.new_order_pricing_plan_name = order_pricing_plan_name
		self.create_order()

	def create_order(self):
		order_notes = {'contact': 'getsetquizindia@gmail.com'}
		new_order =  dict(amount=self.new_order_amount, currency='INR', receipt=self.new_order_receipt, notes=order_notes)
		order = razorpay_client.order.create(new_order)

		self.new_order_id = order.get('id')

	def get_razorpay_order_id(self):

		return new_order_id

	def get_razorpay_order_options(self):
		new_order_options = options
		new_order_options['key'] = str(RAZORPAY_KEY_ID)
		new_order_options['amount'] =  str(self.new_order_amount)
		new_order_options['name'] = str(APP_NAME)
		new_order_options['description'] = str(self.new_order_pricing_plan_name)
		new_order_options['order_id'] = str(self.new_order_id)
		new_order_options['prefill']['name'] = str(self.new_order_client_name)
		new_order_options['prefill']['email'] = str(self.new_order_client_email)

		return json.dumps(new_order_options, indent = 4) #Need to return in JSON for jinja2 to udnerstand.