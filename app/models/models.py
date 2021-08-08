import uuid
from sqlalchemy.dialects.postgresql import UUID
from flask_user import UserMixin
from app import db
from datetime import datetime, date
from sqlalchemy_utils import PhoneNumber

# Define User data-model
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)

    # User Authentication fields
    email = db.Column(db.String(255), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.Date(), nullable=False, default=date.today())
    email_confirmed_at = db.Column(db.DateTime(), nullable=True)
    active = db.Column(db.Boolean, nullable=False, default=True)

    # Relationships
    # # One to one relationship with thhe user profile
    profile = db.relationship('UserProfile', backref="parent_user", uselist=False)
    # One to many relationship with user roles
    roles = db.relationship('Role', secondary='users_roles',
                            backref=db.backref('users', lazy='dynamic'))
    # Subscriptions
    subscriptions = db.relationship('QuizSubscriber', backref="parent_user", lazy='dynamic')
    # Owned Quizzes
    quizzes_owned = db.relationship('QuizOwner', backref="parent_user", lazy='dynamic')
    # Hosted Quizzes
    quizzes_hosted = db.relationship('QuizMaster', backref="parent_user", lazy='dynamic')

# Define the User Profile data-model
class UserProfile(db.Model):
    __tablename__ = 'user_profiles'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))

    # User fields
    profile_complete = db.Column(db.Boolean(), nullable=False, default=True)
    first_name = db.Column(db.String(50), nullable=True, default=u'')
    last_name = db.Column(db.String(50), nullable=True, default=u'')
    institution = db.Column(db.String(250), nullable=True, default=u'')
    nationality = db.Column(db.String(50), nullable=True, default=u'')
    dob = db.Column(db.Date(), nullable=True)
    gender = db.Column(db.String(50), nullable=True, default=u'')
    _phone_number = db.Column(db.Unicode(20), nullable=True)
    country_code = db.Column(db.Unicode(8), nullable=True)
    phone_number = db.composite(
        PhoneNumber,
        _phone_number,
        country_code
    )


# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, server_default=u'', unique=True)
    label = db.Column(db.Unicode(255), server_default=u'')  # for display purposes

# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'users_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

class Quiz(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pricing_plan_id = db.Column(db.Integer(), db.ForeignKey('pricing_plans.id'))
    active = db.Column(db.Boolean(), nullable=False, default=True)
    quiz_completion = db.Column(db.Boolean(), nullable=False, default=False)
    # Relationships
    # One to one relationship to quiz details
    details = db.relationship('QuizDetails', backref="parent_quiz", uselist=False)
    # # One to one relationship to ownner
    quiz_owner = db.relationship('QuizOwner', backref="parent_quiz", uselist=False)
    # # One to one relationship to quizmaster
    quiz_master = db.relationship("QuizMaster", backref="parent_quiz", uselist=False)
    # One to one relationship to quiz standings
    quiz_standings = db.relationship("QuizStandings", backref="parent_quiz", uselist=False)
    # One to one relationship to refund requests
    refund = db.relationship("RefundRequest", backref="parent_quiz", uselist=False)
    # One to many relationship to subscriber
    subscribers = db.relationship('QuizSubscriber', backref="parent_quiz", lazy='dynamic')

class QuizDetails(db.Model):
    __tablename__ = 'quiz_details'
    id = db.Column(db.Integer(), primary_key=True)
    quiz_id = db.Column(UUID(as_uuid=True), db.ForeignKey('quizzes.id', ondelete='CASCADE'))

    # User Fields
    name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date(), nullable=False)
    time = db.Column(db.Time(), nullable=False)
    current_players = db.Column(db.Integer(), nullable=False, default=0)
    subscription_price = db.Column(db.Integer(), nullable=False, default=0)

class QuizSubscriber(db.Model):
    __tablename__ = 'quiz_subscribers'

    id = db.Column(db.Integer(), primary_key=True)
    active = db.Column(db.Boolean(), nullable=True, default=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    quiz_id = db.Column(UUID(as_uuid=True), db.ForeignKey('quizzes.id', ondelete='CASCADE'))
    user_confirm = db.Column(db.Boolean(), nullable=False, default=False)
    payment_amount = db.Column(db.Integer(), nullable=False, default=0)
    payment_status = db.Column(db.Boolean(), nullable=False, default=False)
    payment_date = db.Column(db.Date(), nullable=True)
    payment_time = db.Column(db.Time(), nullable=True)
    razorpay_payment_id = db.Column(db.String(200), nullable=True)
    razorpay_order_id = db.Column(db.String(200), nullable=True)
    razorpay_signature = db.Column(db.String(200), nullable=True)

class QuizMaster(db.Model):
    __tablename__ = 'quiz_masters'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    quiz_id = db.Column(UUID(as_uuid=True), db.ForeignKey('quizzes.id', ondelete='CASCADE'))

    user_confirm = db.Column(db.Boolean(), nullable=True, default=False)
    user_confirm_date = db.Column(db.Date(), nullable=True)
    user_confirm_time = db.Column(db.Time(), nullable=True)

class QuizOwner(db.Model):
    __tablename__ = 'quiz_owners'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    quiz_id = db.Column(UUID(as_uuid=True), db.ForeignKey('quizzes.id', ondelete='CASCADE'))
    payment_amount = db.Column(db.Integer(), nullable=False, default=0)
    payment_date = db.Column(db.Date(), nullable=True)
    payment_time = db.Column(db.Time(), nullable=True)
    payment_status = db.Column(db.Boolean(), nullable=False, default=False)
    razorpay_payment_id = db.Column(db.String(200), nullable=True)
    razorpay_order_id = db.Column(db.String(200), nullable=True)
    razorpay_signature = db.Column(db.String(200), nullable=True)

class QuizStandings(db.Model):
    __tablename__ = 'quiz_standings'

    id = db.Column(db.Integer(), primary_key=True)
    quiz_id = db.Column(UUID(as_uuid=True), db.ForeignKey('quizzes.id', ondelete='CASCADE'))
    first_position = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    second_position = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    third_position = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))

class PricingPlan(db.Model):
    __tablename__ = 'pricing_plans'
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(50), nullable=False, server_default=u'unknown')
    price = db.Column(db.Integer(), nullable=False, default=0)
    payment_required = db.Column(db.Boolean(), nullable=False, default=False)
    popular_plan = db.Column(db.Boolean(), nullable=False, default=False)
    total_players = db.Column(db.Integer(), nullable=False, default=5)
    active = db.Column(db.Boolean(), nullable=False, default=True)
    community_access = db.Column(db.Boolean(), nullable=False, default=False)
    dedicated_support = db.Column(db.Boolean(), nullable=False, default=False)
    monthly_status_reports = db.Column(db.Boolean(), nullable=False, default=False)

    # One to one relationship with quiz owner payments
    children_quizzes = db.relationship('Quiz', backref="parent_pricing_plan", lazy='dynamic')

class RefundRequest(db.Model):
    __tablename__ = 'refund_requests'
    id = db.Column(db.Integer, primary_key=True)

    quiz_id = db.Column(UUID(as_uuid=True), db.ForeignKey('quizzes.id', ondelete='CASCADE'))
    refund_confirm = db.Column(db.Boolean(), nullable=True, default=False)
    request_date = db.Column(db.Date(), nullable=True)
    request_time = db.Column(db.Time(), nullable=True)