from flask import Flask, request, redirect, url_for, Blueprint, render_template

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_user import roles_required
from app.email_manager import CustomEmailManager
from app.models.models import User
from app import user_manager
admin = Blueprint("admin", __name__, static_folder="static", template_folder="templates")

@admin.route('/admin/dashboard', methods=['POST','GET'])
@roles_required('admin')
def admindashboard():

	return render_template('admin/admindashboard.html', user=current_user)

@admin.route('/admin/emails/mass_email', methods=['POST', 'GET'])
@roles_required('admin')
def adminmassemail():
	AllUsers = User.query.all()
	for user in AllUsers:
		CustomEmailManager.send_mass_emails(user, user.email)

	flash('Mass emails sent!')
	return redirect(url_for('admin.admindashboard'))

	return render_template('admin/adminindex.html', user=current_user)

