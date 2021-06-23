from flask import Flask, request, redirect, url_for, Blueprint, render_template

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_user import roles_required
from app import db

user = Blueprint("userdashboard", __name__, static_folder="static", template_folder="templates")

@user.route('/user/dashboard/', methods=['POST','GET'])
@roles_required(['client', 'admin'])
def userdashboardpage():
	user = current_user
	return render_template('user/userdashboard.html', user=user)