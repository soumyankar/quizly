import os

SQLALCHEMY_TRACK_MODIFICATIONS=False
SQLALCHEMY_DATABASE_URI = "postgresql://vgzucsdlhbrbcn:8491ba2aca4676cb76c8a18be7fcf85e4534c1e0ac3e35e16a6c20463745592a@ec2-34-193-113-223.compute-1.amazonaws.com:5432/d17jf8jsppcg3u"
# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SECRET_KEY = "supersecretkey"
# SECRET_KEY = os.environ.get('SECRET_KEY')
SECURITY_PASSWORD_SALT = 'super_duper_secret_key'
BCRYPT_LOG_ROUNDS = 13
WTF_CSRF_ENABLED = True
# Flask-Mail settings
# For smtp.gmail.com to work, you MUST set "Allow less secure apps" to ON in Google Accounts.
# Change it in https://myaccount.google.com/security#connectedapps (near the bottom).
MAIL_SERVER = 'smtp.gmail.com'
# MAIL_PORT = 587
# MAIL_USE_SSL = False
# MAIL_USE_TLS = True
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'getsetquizindia@gmail.com'
MAIL_PASSWORD = 'Gsquiz123'
MAIL_DEFAULT_SENDER = 'getsetquizindia@gmail.com'
# Sendgrid settings
# SENDGRID_API_KEY='place-your-sendgrid-api-key-here'
# Flask-User settings
USER_APP_NAME = 'GetSetQuiz'
USER_EMAIL_SENDER_NAME = 'GetSetQuiz Team'
USER_EMAIL_SENDER_EMAIL = 'getsetquizindia@gmail.com'

ADMINS = [
    '"Administrator" <getsetquizindia@gmail.com>',
    ]

# Razorpay API Creds
RAZORPAY_KEY_ID = "rzp_test_UPoINxBbSVtQlr"
RAZORPAY_KEY_SECRET = "wnFS8R0i91wva9viP9pXjkyx"