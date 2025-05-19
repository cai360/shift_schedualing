from flask import Blueprint, render_template, request, redirect, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from helper import apology, login_required


bp = Blueprint("auth", __name__)

@bp.route("/")
@login_required
def index():
    """ to show the current month's schedual"""
    return render_template("index.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]
        session["role"] = rows[0]["role"]

        return redirect("/")

    else:
        return render_template("login.html")
    

@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")



@bp.route("/changePassword", methods=["GET", "POST"])
@login_required
def changePassword():
    """to change password"""
    if request.method == "GET":
        return render_template("changePassword.html")
    else:
        userID = session["user_id"]
        # get the current password and new password
        if not request.form.get("current_password"):
            return apology("Must provide current password", 403)
        elif not request.form.get("new_password"):
            return apology("Must provide password", 403)

        elif not request.form.get("passwordConfirm"):
            return apology("Must confirm your new password", 403)

         # check is the userID and password matches
        rows = db.execute(
            "SELECT * FROM users WHERE id = ?", userID)

        # to check if current password is correct
        hash = db.execute("SELECT hash FROM users WHERE id = ?", userID)

        if not check_password_hash(hash[0]["hash"], request.form.get("current_password")):
            return apology("Password incorrect")

         # check is the new password and the confirmation are match
        if request.form.get("new_password") != request.form.get("passwordConfirm"):
            return apology("New password do not match")

         # change the password
        else:
            db.execute("UPDATE users SET hash=? WHERE id=?", generate_password_hash(
                request.form.get("passwordConfirm")), userID)
            flash("Succese!")

        return redirect("/")


@bp.route("/forgetPassword")
def forgetPassword():
    """to recover password"""
    return apology("TODO")


