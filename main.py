from __future__ import print_function # For printing to console. !!Must be placed on beginning of file!!

from flask import Flask, Blueprint, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from jinja2 import TemplateNotFound

# OS Libraries
import sys
import os

# Import src python files
from src.homepage import homepage

app = Flask(__name__)
app.register_blueprint(homepage, url_prefix="")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run()