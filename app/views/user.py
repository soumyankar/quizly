from flask import Flask, request, redirect, url_for, Blueprint, render_template

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_user import roles_required
from app import db

user = Blueprint("user_dashboard", __name__, static_folder="static", template_folder="templates")

@user.route('/user/dashboard/', methods=['POST','GET'])
@login_required
def user_dashboard_page():
	user = current_user
	return render_template('user/user_homepage.html', user=user)