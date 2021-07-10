from .admin import admin
from .homepage import homepage
from .quiz import quiz
from .user import user_dashboard
from .errorhandler import errorhandler

def register_blueprints(app):
    app.register_blueprint(homepage)
    app.register_blueprint(quiz)
    app.register_blueprint(user_dashboard)
    app.register_blueprint(admin)
    app.register_blueprint(errorhandler)