from __future__ import print_function # For printing to console. !!Must be placed on beginning of file!!

from flask import Flask, Blueprint, render_template, url_for
from jinja2 import TemplateNotFound

# OS Libraries
import sys
import os

# Import src python files
from src.homepage import homepage
from src.adminlogin import adminlogin, db, login_manager
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') # os.environ.get('DATABASE_URL') #'sqlite:///test.db' # 3 forward slashes means relative path; 4 forward slashes means exact path
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.cli.add_command(create_tables)
Bootstrap(app)
db.init_app(app)
login_manager.init_app(app)

app.register_blueprint(homepage, url_prefix="")
app.register_blueprint(adminlogin, url_prefix="")
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run()