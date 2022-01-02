from flask import render_template


class ErrorHandler:

    @staticmethod
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @staticmethod
    def not_found(e):
        return render_template('errors/404.html'), 404

    @staticmethod
    def server_error(e):
        return render_template('errors/500.html'), 500
