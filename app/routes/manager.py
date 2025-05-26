from flask import Blueprint, render_template, request, redirect, session, flash
from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta, date
import random
import string
from schedule import Schedule
from helper import login_required, apology



bp = Blueprint("manager", __name__)

@bp.route("/manageUsers", methods=["GET", "POST"])
@login_required
def toManageUsers():
    """to add employee or manager into system"""

    employeelist = db.execute("SELECT username, user_id, department, role  FROM users")

    if request.method == "GET":
        return render_template("manage_user.html", employeelist = employeelist)
    else:
        mode = request.form.get("action")
        username = request.form.get("username")
        userID = request.form.get("user_id")
        role = "employee"

        if mode == "add":
            # generate a temporary password, lengh: k=8
            password = ''.join(random.choices(
                string.ascii_letters + string.digits, k=8))

            hash = generate_password_hash(password)

            # register the user
            db.execute(
                "INSERT INTO users (username, user_id, hash, role) VALUES(?, ?, ?, ?)", username, userID, hash, role)

            flash("success! ")
            flash("temporary password: " + password)

        elif mode == "delete":
             row = db.execute("SELECT * FROM users WHERE username = ? AND user_id = ?",
             username, request.form.get("user_id"))

             if len(row) == 0:
                return apology("User not found")
             else:
                db.execute("DELETE FROM users WHERE username = ? AND user_id = ?",
                        request.form.get("username"), request.form.get("user_id"))
                
             flash("deleted!")

        newList = db.execute("SELECT username, user_id, department, role FROM users")
                      
        return render_template("manage_user.html", employeelist = newList)
    
        

@bp.route("/create_empty_shifts", methods=["GET", "POST"])
@login_required
def create_empty_shifts():

    """create the empty shifts"""

    current_date = datetime.today()

    # Calculate next month
    next = current_date.replace(day=1) + timedelta(days=32)
    default_year = next.year
    default_month = next.month
    
    default_interval = 1

    if request.method == "GET":
        return render_template("create_empty_shifts.html", default_year=default_year, default_month=default_month, default_interval=default_interval)

    else:
        year = int(request.form.get("year"))
        if not year:
            year = current_date.year

        if int(year) < 0:
            return apology("Ivaliad year")

        month = int(request.form.get("month"))

        if not month:
            return apology("Month must be given")
        
        if month > 12 or month < 1:
            return apology("Ivaliad month")

        starting_hour =  int(request.form.get("starting_hour"))
        if not starting_hour:
            return apology("Starting hour must be given")

        ending_hour = int(request.form.get("ending_hour"))
        if not ending_hour:
            return apology("ending hour must be given")
        elif ending_hour <= starting_hour:
            return apology("Ending hour must be greater than starting hour")

        interval = int(request.form.get("interval"))
        if not interval:
            return apology("Interval must be given")
        elif (ending_hour - starting_hour) % interval != 0:
            return apology("Working hours must be a multiple of the interval you set.")

        rest_weeks = request.form.getlist('rest_weeks')
        rest_weeks_int = list(map(int, rest_weeks))



        try:
            sched = Schedule(year, month, starting_hour, ending_hour, interval)
            shifts = sched.generate_shifts()
            shifts = sched.rest_dates(rest_weeks_int)
            col = sched.hour_interval()
        except ValueError as e:
            return apology(str(e))
        
        session["shifts"] = shifts
        session["year"] = year
        session["month"] = month
        session["start"] = starting_hour
        session["end"] = ending_hour
        session["interval"] = interval
        session["free_dates"] = sched.get_free_dates()
        session["col"] = col
        
        return redirect("/modified_empty_shifts")
    


@bp.route("/modified_empty_shifts", methods=["GET", "POST"])
@login_required
def modified_empty_shifts(): 
    year = session.get("year")
    month = session.get("month")
    free_dates = session.get("free_dates", []).copy()
    shifts = session.get("shifts", []).copy()
    col = session.get("col", [])

    if not year or not month:
        return apology("Session expired. Please restart the process.")

    if request.method == "GET":
        if not shifts:
            return render_template("create_empty_shifts.html")
        return render_template("create_empty_shifts2.html", datelist=sorted(shifts), year=year, month=month, col=col)

    if request.form.get("previous"):
        return redirect("/create_empty_shifts")

    mode = request.form.get("action")
    modified_value = request.form.get("modified")

    month_str = str(month).zfill(2)
    day_str = str(modified_value).zfill(2)
    date_s = f"{year}-{month_str}-{day_str}"

    if not Schedule.is_valid_date(date_s):
        return apology("Invalid date")

    d = date(year, month, int(modified_value))
    weekday = d.weekday()
    value = (int(modified_value), weekday)

    if mode == "add":
        if value in free_dates:
            free_dates.remove(value)
        if value not in shifts:
            shifts.append(value)
        else: 
            flash("Date already exists")
    elif mode == "delete":
        if value in shifts:
            shifts.remove(value)
            if value not in free_dates:
                free_dates.append(value)
        else:
            flash("Date doesn't exist")

    session["free_dates"] = free_dates
    session["shifts"] = sorted(shifts)

    return render_template("create_empty_shifts2.html", datelist=sorted(shifts), year=year, month=month, col=col)



@bp.route("/assign_shifts", methods=["GET", "POST"])
@login_required
def assign_shifts():
    """assign the shifts"""
    return apology("TODO")


@bp.route("/change_shift_m", methods=["GET", "POST"])
@login_required
def change_shift_m():
    """to change the shifts after assigned """
    return apology("TODO")


@bp.route("/approved_requests", methods=["GET", "POST"])
@login_required
def approved_requests():
    """to approved changing shift request"""
    return apology("TODO")


@bp.route("/history", methods=["GET", "POST"])
@login_required
def history():
    """to review history or worker shift"""
    return apology("TODO")


@bp.route("/print", methods=["GET", "POST"])
@login_required
def print():
    """to print all the forms inculding monthly shift and workers form"""
    return apology("TODO")
