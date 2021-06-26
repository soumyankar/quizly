"""This module implements the EmailManager for Flask-User.
It uses Jinja2 to render email subject and email message.
It uses the EmailAdapter interface to send emails.
"""

# Author: Ling Thio <ling.thio@gmail.com>
# Copyright (c) 2013 Ling Thio
from flask_user import EmailManager
from flask import render_template, url_for

from flask_user import ConfigError

# The UserManager is implemented across several source code files.
# Mixins are used to aggregate all member functions into the one UserManager class.
class CustomEmailManager(EmailManager):
    """ Send emails via the configured EmailAdapter ``user_manager.email_adapter``. """
    def send_mass_emails(self, user, user_email):
        # Verify config settings
        if not self.user_manager.USER_ENABLE_EMAIL: return
        if not self.user_manager.USER_ENABLE_CONFIRM_EMAIL: return

        # The confirm_email email is sent to a specific user_email.email or user.email
        email = user_email.email if user_email else user.email
        random_token="This is just some random crap."
        # Render email from templates and send it via the configured EmailAdapter
        self._render_and_send_email(
            email,
            user,
            self.user_manager.USER_MASS_EMAIL_TEMPLATE,
            random_token=random_token,
        )