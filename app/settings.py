# Settings common to all environments (development|staging|production)
# Place environment specific settings in env_settings.py
# An example file (env_settings_example.py) can be used as a starting point

import os

# Application settings
BANNER_APP_NAME ="E T S E T Q U I Z "
APP_NAME = "GetSetQuiz"
APP_SYSTEM_ERROR_SUBJECT_LINE = APP_NAME + " system error"

# Flask settings
CSRF_ENABLED = True

# Flask-SQLAlchemy settings
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask-User settings
USER_APP_NAME = APP_NAME
USER_ENABLE_CHANGE_PASSWORD = True  # Allow users to change their password
USER_ENABLE_CHANGE_USERNAME = True  # Allow users to change their username
USER_ENABLE_CONFIRM_EMAIL = True  # Force users to confirm their email
USER_ENABLE_FORGOT_PASSWORD = True  # Allow users to reset their passwords
USER_ENABLE_EMAIL = True  # Register with Email
USER_ENABLE_REGISTRATION = True  # Allow new users to register
USER_REQUIRE_RETYPE_PASSWORD = True  # Prompt for `retype password` in:
USER_ENABLE_USERNAME = False  # Register and Login with username
USER_EDIT_USER_PROFILE_TEMPLATE = 'user/user_settings.html'
USER_CHANGE_PASSWORD_TEMPLATE = 'user/user_settings.html'
USER_CHANGE_USERNAME_TEMPLATE = 'user/user_settings.html'
USER_AFTER_LOGIN_ENDPOINT = 'user_dashboard.user_dashboard_page'
USER_AFTER_LOGOUT_ENDPOINT = 'homepage.index'
USER_UNAUTHENTICATED_ENDPOINT = 'user.login'
USER_UNAUTHORIZED_ENDPOINT = 'user.login'
# USER_AFTER_EDIT_USER_PROFILE_ENDPOINT = 'user_dashboard.user_profile_page'
USER_AFTER_CONFIRM_ENDPOINT = 'user.edit_user_profile'