from flask import Flask, request, redirect, url_for, Blueprint, render_template

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_user import roles_required
from app import db

admin = Blueprint("admin", __name__, static_folder="static", template_folder="templates")

@admin.route('/admin/dashboard', methods=['POST','GET'])
@roles_required('admin')
def admindashboard():
	return render_template('admin/adminindex.html', user=current_user)