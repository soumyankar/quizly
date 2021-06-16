from __future__ import print_function # For printing to console. !!Must be placed on beginning of file!!

# Flask libraries
from flask import Flask
from flask_bootstrap import Bootstrap
import psycopg2

# OS Libraries
import sys
import os

# Routes
from src.routes.homepage import homepage
from src.routes.admin import admin
from src.routes.adminlogin import adminlogin
from src.routes.adminlogout import adminlogout
from src.routes.quiz import quiz
from src.routes.quizregister import quizregister
from src.routes.quizplans import quizplans

# Extensions
from src.extensions import db,login_manager
from src.models import Admin

app = Flask(__name__)
app.config.from_pyfile("src/settings.py")

Bootstrap(app)
db.init_app(app)

with app.app_context():
    db.create_all()

login_manager.init_app(app)
login_manager.login_view = 'adminloginPage'
@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get((user_id))

# Register blueprints here.
app.register_blueprint(homepage, url_prefix="")
app.register_blueprint(admin, url_prefix="")
app.register_blueprint(adminlogin, url_prefix="")
app.register_blueprint(adminlogout, url_prefix="")
app.register_blueprint(quiz, url_prefix="")
app.register_blueprint(quizregister, url_prefix="")
app.register_blueprint(quizplans, url_prefix="")
if __name__ == "__main__":
    app.run()