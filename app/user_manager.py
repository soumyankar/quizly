from flask import current_app
from flask_login import current_user
from flask_user import UserManager
from wtforms import ValidationError

# Customize Flask-User 
class CustomUserManager(UserManager):
    def __init__(self, app, db, UserClass, **kwargs):
        self.app = app
        if app:
            self.init_app(app, db, UserClass, **kwargs)

    def edit_user_profile_view(self):
        # Initialize form
        form = self.EditUserProfileFormClass(request.form, obj=current_user)

        # Process valid POST
        if request.method == 'POST' and form.validate():
            # Update fields
            return redirect(self._endpoint_url(self.USER_AFTER_EDIT_USER_PROFILE_ENDPOINT))

        return render_template(self.USER_EDIT_USER_PROFILE_TEMPLATE, form=form)

    def customize(self, app):
        from .forms.forms import CustomRegisterForm, CustomUserProfileForm, CustomLoginForm, CustomChangePasswordForm
        # Configure customized forms
        self.RegisterFormClass = CustomRegisterForm
        self.UserProfileFormClass = CustomUserProfileForm
        # self.LoginFormClass = CustomLoginForm
        self.ChangePasswordForm = CustomChangePasswordForm
        # NB: assign:  xyz_form = XyzForm   -- the class!
        #   (and not:  xyz_form = XyzForm() -- the instance!)