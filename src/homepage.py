from flask import Flask, request, redirect, url_for, Blueprint, render_template

import time
import json
homepage = Blueprint("homepage", __name__, static_folder="../static", template_folder="../templates")

@homepage.route("/", methods=['GET'])
def index():
	return render_template('index.html')