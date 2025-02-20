from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
import random
import string

from helper import login_required, apology




# Configure application
app = Flask(__name__)
db = SQL("sqlite:///shift_schedualing.db")

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


@app.route("/")
@login_required
def index():
    """ to show the current month's schedual"""
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
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

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/forgetPassword")
def forgetPassword():
    return apology("TODO")
    

@app.route("/changePassword", methods=["GET", "POST"])
@login_required
def changePassword():
    """to change password"""
    if request.method == "GET":
        return render_template("changePassword.html")
    else:
        userID = session["user_id"]
        #get the current password and new password
        if not request.form.get("current_password"):
            return apology("Must provide current password", 403)
        elif not request.form.get("new_password"):
            return apology("Must provide password", 403)
        
        elif not request.form.get("passwordConfirm"):
            return apology("Must confirm your new password", 403)

         #check is the userID and password matches
        rows = db.execute(
            "SELECT * FROM users WHERE id = ?", userID)

         #to check if current password is correct
        hash = db.execute("SELECT hash FROM users WHERE id = ?", userID)

        if not check_password_hash(hash[0]["hash"], request.form.get("current_password")):
            return apology("Password incorrect")

         #check is the new password and the confirmation are match
        if request.form.get("new_password") != request.form.get("passwordConfirm"):
            return apology("New password do not match")
        
         #change the password
        else:
            db.execute("UPDATE users SET hash=? WHERE id=?", generate_password_hash(request.form.get("passwordConfirm")), userID)
            flash("Succese!")

        return redirect("/")


"""
function for manager
"""

@app.route("/register", methods=["GET", "POST"])
@login_required
def register():
    """to add employee or manager into system"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        role = request.form.get("role")

        #generate a temporary password, lengh: k=8 
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        hash = generate_password_hash(password)

        #register the user
        db.execute("INSERT INTO users (username, hash, role) VALUES(?, ?, ?)", username, hash, role)


        flash("success! ")
        flash("temporary password: "+ password)
        return render_template("register.html")

@app.route("/delete_user", methods=["GET", "POST"])
@login_required
def delete_user():
    """to delete employee or manager from system"""
    if request.method == "GET":
        return render_template("delete_user.html")
    else:
        if not request.form.get("username"):
            return apology("must provide username", 403)

        elif not request.form.get("user_id"):
            return apology("must provide user ID", 403)

        #delete the user
        row = db.execute("SELECT * FROM users WHERE username = ? AND user_id = ?", request.form.get("username"), request.form.get("user_id"))

        if len(row) == 0:
            return apology("User not found")
        else:
            db.execute("DELETE FROM users WHERE username = ? AND user_id = ?", request.form.get("username"), request.form.get("user_id"))
            flash("deleted!")
            return render_template("delete_user.html")


@app.route("/create_empty_shifts", methods=["GET", "POST"])
@login_required
def create_empty_shifts():
    """create the empty shifts"""
    if request.method == "GET":
        current_date = datetime.today()

        # Calculate next month
        next_month = current_date.replace(day=1) + timedelta(days=32)
        default_year = next_month.year
        default_month = next_month.month

        return render_template("create_empty_shifts.html", default_year=default_year, default_month=default_month)
    else:


        year = request.form.get("year")
        if not year:
            year = current_date.year
        
        if int(year) < 0:
            return apology("Ivaliad year")


        # month = request.form.get("month")
        # if not month:
        #     month = current_date.month

        # if month < 1 or month > 12:
        #     return apology("Ivaliad month")
        
   
        # startTime = request.form.get("startTime")
        # if not startTime:
        #     return apology("start time must be given")
        # if startTime > 23 or startTime < 0:
        #     return apology("Invaliad starting time")
        
        # endTime = request.form.get("endTime")
        # if not endTime:
        #     return apology("end time must be given")
        # if endTime > 24 or endTime < startTime:
        #     return apology("Ivaliad endTime")
        
        # interval = request.form.get("interval")
        # if not interval:
        #     return apology("Interval must be given")
        

        return render_template("create_empty_shifts.html")
        

    return apology("TODO")

@app.route("/assign_shifts", methods=["GET", "POST"])
@login_required
def assign_shifts():
    """assign the shifts"""
    return apology("TODO")

@app.route("/change_shift_m", methods=["GET", "POST"])
@login_required
def change_shift_m():
    """to change the shifts after assigned """
    return apology("TODO")


@app.route("/approved_requests", methods=["GET", "POST"])
@login_required
def approved_requests():
    """to approved changing shift request"""
    return apology("TODO")


@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    """to review history or worker shift"""
    return apology("TODO")


@app.route("/print", methods=["GET", "POST"])
@login_required
def print():
    """to print all the forms inculding monthly shift and workers form"""
    return apology("TODO")


"""
function for employee
"""

@app.route("/pick_up_shift", methods=["GET", "POST"])
@login_required
def pick_up_shifte():
    """pick up shift"""
    return apology("TODO")


@app.route("/change_shift_e", methods=["GET", "POST"])
@login_required
def change_shift_e():
    """ask for taking shift or take over shift"""
    return apology("TODO")


@app.route("/comfirm_schedule", methods=["GET", "POST"])
@login_required
def comfirm_schedule():
    """to comfirm the schedual, which has time limit (after 3 days the schedual publish)"""
    return apology("TODO")

if __name__ == '__main__':
    app.debug = True
    app.run()

