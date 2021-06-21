from flask import Blueprint, render_template

errorhandler = Blueprint('errorhandler', __name__)


@errorhandler.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404


@errorhandler.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403


@errorhandler.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500