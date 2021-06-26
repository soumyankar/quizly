# This file defines command line commands for manage.py
#
# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

import datetime
from flask import current_app
from flask_script import Command

from app import db
from app.models.models import User, Role, UserRoles, Quiz, PricingPlan
# from app.models.pricingplan_models import PricingPlan

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
    
    # Add users
    user = find_or_create_user(u'getsetquizindia@gmail.com', u'getsetquiz9999', u'supersecretpass')
    user = find_or_create_user(u'soumyankarm@gmail.com', u'client9999', u'supersecretpass')

    # Add Pricing Plans
    pricingplan = find_or_create_pricingplan(u'Basic', 0, False, False, 20, True)
    pricingplan = find_or_create_pricingplan(u'Premium', 150, True, True, 100, True)
    # Save to DB
    db.session.commit()


def find_or_create_role_user(name, label):
    """ Find existing role or create new role """
    role = Role.query.filter(Role.name == name).first()
    if not role:
        role = Role(name=name, label=label)
        db.session.add(role)
    return role

def find_or_create_pricingplan(name, price, payment_required, popular_plan, total_players, active):
    """ Find or create the pricing plans for quizzes """
    plan = PricingPlan.query.filter(PricingPlan.name == name).first()
    if not plan:
        plan = PricingPlan(name=name, price=price, payment_required=payment_required, popular_plan=popular_plan, total_players=total_players, active=active)
        db.session.add(plan)
    return plan

def find_or_create_user(email, username, password, role=None):
    """ Find existing user or create new user """
    new_user = User.query.filter(User.email == email).first()
    if not new_user:
        new_user = User(
            email=email,
            password=current_app.user_manager.password_manager.hash_password(password),
            active=True,
            registered_on=datetime.datetime.now(),
            email_confirmed_at=datetime.datetime.now(),
            username=username
            )
        if role:
            new_user.roles.append(role)
        db.session.add(new_user)
    return new_user
