from flask_user import UserMixin
from app import db
from datetime import datetime, date

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
    profile_id = db.Column(db.Integer(), db.ForeignKey('user_profiles.id'))
    profile = db.relationship('UserProfile', uselist=False)
    # One to many relationship with user roles
    roles = db.relationship('Role', secondary='users_roles',
                            backref=db.backref('users', lazy='dynamic'))
    # Subscriptions
    subscriptions = db.relationship('Quiz', secondary='quiz_subscriptions',
                                    backref=db.backref('users', lazy='dynamic'))

# Define the User Profile data-model
class UserProfile(db.Model):
    __tablename__ = 'user_profiles'

    id = db.Column(db.Integer(), primary_key=True)

    # User fields
    profile_complete = db.Column(db.Boolean(), nullable=False, default=True)
    first_name = db.Column(db.String(50), nullable=False, default=u'')
    last_name = db.Column(db.String(50), nullable=False, default=u'')
    instituion = db.Column(db.String(250), nullable=True, default=u'')
    nationality = db.Column(db.String(50), nullable=False, default=u'')
    age = db.Column(db.Integer(), nullable=False, default=-1)
    gender = db.Column(db.String(50), nullable=False, default=u'')

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
    id = db.Column(db.Integer(), primary_key=True)

    uuid = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date(), nullable=False)
    time = db.Column(db.Time(), nullable=False)
    # Relationships
    # One to one relationship to ownner
    owner = db.Column(db.Integer(), db.ForeignKey('quiz_owners.id'))
    # One to one relationship to quizmaster
    quiz_master = db.Column(db.Integer(), db.ForeignKey('quiz_masters.id'))
    # One to one relationship to quiz_winner
    quiz_winner = db.Column(db.Integer(), db.ForeignKey('quiz_winners.id'))
    # One to one relationship to pricing plan
    pricing_plan = db.Column(db.Integer(), db.ForeignKey('pricing_plans.id'))
    # Many to many relationship to subscriber
    subscribers = db.relationship('User', secondary='quiz_subscribers', 
                            backref=db.backref('quiz', lazy='dynamic'))

class QuizSubscription(db.Model):
    __tablename__ = 'quiz_subscriptions'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    quiz_id = db.Column(db.Integer(), db.ForeignKey('quizzes.id', ondelete='CASCADE'))

class QuizSubscriber(db.Model):
    __tablename__ = 'quiz_subscribers'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    quiz_id = db.Column(db.Integer(), db.ForeignKey('quizzes.id', ondelete='CASCADE'))
    user_confirm = db.Column(db.Boolean(), nullable=False, default=False)
    payment_status = db.Column(db.Boolean(), nullable=False, default=False)

class QuizMaster(db.Model):
    __tablename__ = 'quiz_masters'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    quiz_id = db.Column(db.Integer(), db.ForeignKey('quizzes.id', ondelete='CASCADE'))
    quiz_master_confirm = db.Column(db.Boolean(), nullable=True, default=False)

class QuizOwner(db.Model):
    __tablename__ = 'quiz_owners'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    quiz_id = db.Column(db.Integer(), db.ForeignKey('quizzes.id', ondelete='CASCADE'))

class QuizWinner(db.Model):
    __tablename__ = 'quiz_winners'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    quiz_id = db.Column(db.Integer(), db.ForeignKey('quizzes.id', ondelete='CASCADE'))

class PricingPlan(db.Model):
    __tablename__ = 'pricing_plans'
    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(50), nullable=False, server_default=u'unknown')
    price = db.Column(db.Integer(), nullable=False, default=0)
    payment_required = db.Column(db.Boolean(), nullable=False, default=False)
    popular_plan = db.Column(db.Boolean(), nullable=False, default=False)
    total_players = db.Column(db.Integer(), nullable=False, default=5)
    active = db.Column(db.Boolean(), nullable=False, default=True)


