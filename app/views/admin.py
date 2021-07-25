from flask import Flask, request, redirect, url_for, Blueprint, render_template

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_user import roles_required
from app.email_manager import CustomEmailManager
from app.models.models import User
from app.db_commands.user_commands import *
from app.db_commands.quiz_commands import *
from app import user_manager

admin = Blueprint("admin", __name__, static_folder="static", template_folder="templates")

@admin.route('/admin/dashboard', methods=['POST','GET'])
@roles_required('admin')
def admin_dashboard():
	return render_template('admin/admin_dashboard.html', user=current_user)

@admin.route('/admin/user/quiz_owners', methods=['POST', 'GET'])
@roles_required('admin')
def admin_user_quiz_owners():
	all_quiz_owners = get_all_quiz_owners()
	return render_template('admin/admin_user_quiz_owners.html', user=current_user, all_quiz_owners=all_quiz_owners)

@admin.route('/admin/emails/mass_email', methods=['POST', 'GET'])
@roles_required('admin')
def adminmassemail():
	AllUsers = User.query.all()
	for user in AllUsers:
		CustomEmailManager.send_mass_emails(user, user.email)

	flash('Mass emails sent!')
	return redirect(url_for('admin.admindashboard'))

	return render_template('admin/adminindex.html', user=current_user)

