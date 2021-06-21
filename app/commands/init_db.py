# This file defines command line commands for manage.py
#
# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

import datetime

from flask import current_app
from flask_script import Command

from app import db
from app.models.user_models import User, Role
from app.models.quiz_models import Quiz, QuizRole
from app.models.pricingplan_models import PricingPlan

class InitDbCommand(Command):
    """ Initialize the database."""

    def run(self):
        init_db()
        print('Database has been initialized.')

def init_db():
    """ Initialize the database."""
    db.drop_all()
    db.create_all()
    create_users()


def create_users():
    """ Create users """

    # Create all tables
    db.create_all()

    # Adding user roles
    admin_role = find_or_create_role_user('admin', u'Admin')
    client_role = find_or_create_role_user('client', u'Client')

    # Adding quiz player/owner roles
    owner_role = find_or_create_role_quiz('owner', u'Owner')
    player_role = find_or_create_role_quiz('player' u'Player')
    
    # Add users
    user = find_or_create_user(u'GetSetQuiz', u'Admin', u'getsetquizindia@gmail.com', 'supersecretpass', 'getsetquiz9999', '9999', 'Others', 'India', admin_role)
    user = find_or_create_user(u'Client', u'Example', u'soumyankarm@gmail.com', 'supersecretpass', 'client9999', '9999', 'Others', 'India', client_role)

    # Add Pricing Plans
    pricingplan = find_or_create_pricingplan(u'Basic', 0, False, 20)
    pricingplan = find_or_create_pricingplan(u'Premium', 150, True, 100)
    # Save to DB
    db.session.commit()


def find_or_create_role_user(name, label):
    """ Find existing role or create new role """
    role = Role.query.filter(Role.name == name).first()
    if not role:
        role = Role(name=name, label=label)
        db.session.add(role)
    return role

def find_or_create_role_quiz(name, label):
    """ Find existing role or create new role """
    role = QuizRole.query.filter(QuizRole.name == name).first()
    if not role:
        role = QuizRole(name=name, label=label)
        db.session.add(role)
    return role

def find_or_create_pricingplan(name, price, payment_required, total_players):
    """ Find or create the pricing plans for quizzes """
    plan = PricingPlan.query.filter(PricingPlan.name == name).first()
    if not plan:
        plan = PricingPlan(name=name, price=price, payment_required=payment_required, total_players=total_players)
        db.session.add(plan)
    return plan

def find_or_create_user(first_name, last_name, email, password, username, age, gender, nationality, role=None):
    """ Find existing user or create new user """
    user = User.query.filter(User.email == email).first()
    if not user:
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=current_app.user_manager.password_manager.hash_password(password),
            active=True,
            email_confirmed_at=datetime.datetime.now(),
            username=username,
            age=age,
            gender=gender,
            confirmed=True,
            nationality=nationality,
            registered_on=datetime.datetime.now()
            )
        if role:
            user.roles.append(role)
        db.session.add(user)
    return user
