import sys
sys.path.append("..")
from flask import Flask, request, redirect, url_for, Blueprint, render_template

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from src.extensions import db, login_manager

admin = Blueprint("admin", __name__, static_folder="../../static", template_folder="../../templates")

@admin.route('/admin/', methods=['POST','GET'])
@login_required
def admindashboard():
	return render_template('admin.html')