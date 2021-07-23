from functools import wraps
from flask import g, request, redirect, url_for, flash
from flask_login import current_user
from app.db_commands.user_commands import *

def profile_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		user_profile = get_user_profile(current_user.id)
		if not user_profile or user_profile.profile_complete == False:
			flash('Please <a href="'+url_for('user.edit_user_profile')+'">complete your profile</a> otherwise you may not be allowed to <b>Create a Quiz</b> or <b>Subscribe to a Quiz</b>.', 'error')
			return redirect(url_for('user.edit_user_profile'))
		return f(*args,**kwargs)
	return decorated_function