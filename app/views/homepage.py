from flask import Flask, request, redirect, url_for, Blueprint, render_template

homepage = Blueprint("homepage", __name__, static_folder="static", template_folder="templates")

@homepage.route("/", methods=['GET'])
def index():
	return render_template('homepage/index.html')

@homepage.route("/contact-us", methods=['GET'])
def contact():
	return render_template('homepage/contact_us.html')


@homepage.route("/userdashboard", methods=['GET'])
def userindex():
	return render_template('user/userindex.html')
	
@homepage.route("/userpass", methods=['GET'])
def userpasschange():
	return render_template('flask_user/change_password.html')


