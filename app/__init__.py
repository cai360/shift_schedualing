from cs50 import SQL
from flask import Flask, request, session
from flask_session import Session


# Configure application
db = SQL("sqlite:///shift_schedualing.db")



def create_app():
    app = Flask(__name__)
    # Configure session to use filesystem (instead of signed cookies)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    @app.after_request
    def after_request(response):
        """Ensure responses aren't cached"""
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response
    
    from .routes import auth, manager, employee
    app.register_blueprint(auth.bp)
    app.register_blueprint(manager.bp)
    app.register_blueprint(employee.bp)

    return app

