from flask import current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from flask_user import UserManager
from wtforms import ValidationError
from app import db
from app.db_commands.user_commands import *

# Customize Flask-User 
class CustomUserManager(UserManager):
    def __init__(self, app, db, UserClass, **kwargs):
        self.app = app
        if app:
            self.init_app(app, db, UserClass, **kwargs)

    
    @login_required
    def edit_user_profile_view(self):
        # Initialize form
        form = self.EditUserProfileFormClass
        if user_profile_exists(current_user):
            user_profile = get_user_profile(current_user.id)
            form = self.EditUserProfileFormClass(obj=user_profile)
        # Process valid POST
        if request.method == 'POST':
            # Update fields
            if not form.validate():
                flash('There was a problem with one of the input fields, try again', 'error')
                return redirect(url_for('user.edit_user_profile'))

            create_new_user_profile(form, current_user)
            flash('Profile updated!', 'success')
            # return redirect(self._endpoint_url(self.USER_AFTER_EDIT_USER_PROFILE_ENDPOINT))
            return redirect(url_for('user_dashboard.user_profile_page', username=current_user.username))
        # Check if details already exist.
        return render_template(self.USER_EDIT_USER_PROFILE_TEMPLATE, form=form, import_form="edit_user_profile")

    @login_required
    def change_password_view(self):
        """ Prompt for old password and new password and change the user's password."""

        # Initialize form
        form = self.ChangePasswordFormClass(request.form)

        # Process valid POST
        if request.method == 'POST':
            if not form.validate():
                flash(('There was an error changing your password.'), 'error')
                return redirect(url_for('user.change_password'))

            # Hash password
            new_password = form.new_password.data
            password_hash = self.hash_password(new_password)

            # Update user.password
            current_user.password = password_hash
            self.db_manager.save_object(current_user)
            self.db_manager.commit()

            # Send password_changed email
            if self.USER_ENABLE_EMAIL and self.USER_SEND_PASSWORD_CHANGED_EMAIL:
                self.email_manager.send_password_changed_email(current_user)

            # Send changed_password signal
            signals.user_changed_password.send(current_app._get_current_object(), user=current_user)

            # Flash a system message
            flash(_('Your password has been changed successfully.'), 'success')

            # Redirect to 'next' URL
            safe_next_url = self._get_safe_next_url('next', self.USER_AFTER_CHANGE_PASSWORD_ENDPOINT)
            return redirect(safe_next_url)

        # Render form
        return render_template(self.USER_CHANGE_PASSWORD_TEMPLATE, form=form, import_form="change_password")

    @login_required
    def change_username_view(self):
        """ Prompt for new username and old password and change the user's username."""

        # Initialize form
        form = self.ChangeUsernameFormClass(request.form)

        # Process valid POST
        if request.method == 'POST' and form.validate():
            # Change username
            new_username = form.new_username.data
            current_user.username=new_username
            self.db_manager.save_object(current_user)
            self.db_manager.commit()

            # Send username_changed email
            if self.USER_ENABLE_EMAIL and self.USER_SEND_USERNAME_CHANGED_EMAIL:
                self.email_manager.send_username_changed_email(current_user)

            # Send changed_username signal
            signals.user_changed_username.send(current_app._get_current_object(), user=current_user)

            # Flash a system message
            flash(_("Your username has been changed to '%(username)s'.", username=new_username), 'success')

            # Redirect to 'next' URL
            safe_next_url = self._get_safe_next_url('next', self.USER_AFTER_CHANGE_USERNAME_ENDPOINT)
            return redirect(safe_next_url)

        # Render form
        self.prepare_domain_translations()
        return render_template(self.USER_CHANGE_USERNAME_TEMPLATE, form=form, import_form="change_username")


    def customize(self, app):
        from .forms.forms import CustomRegisterForm, CustomUserProfileForm, CustomLoginForm, CustomChangePasswordForm
        # Configure customized forms
        self.RegisterFormClass = CustomRegisterForm
        self.EditUserProfileFormClass = CustomUserProfileForm
        # self.LoginFormClass = CustomLoginForm
        # self.ChangePasswordForm = CustomChangePasswordForm
        # NB: assign:  xyz_form = XyzForm   -- the class!
        #   (and not:  xyz_form = XyzForm() -- the instance!)