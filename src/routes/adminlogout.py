import sys
sys.path.append("..")

from flask import Flask, request, redirect, url_for, Blueprint, render_template
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from src.extensions import db, login_manager

adminlogout = Blueprint("adminlogout", __name__, static_folder="../../static", template_folder="../../templates")

@adminlogout.route("/admin/logout", methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage.index'))