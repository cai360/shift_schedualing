from flask import Blueprint
from helper import login_required, apology


bp = Blueprint("employee", __name__)

@bp.route("/pick_up_shift", methods=["GET", "POST"])
@login_required
def pick_up_shifte():
    """pick up shift"""
    return apology("TODO")


@bp.route("/change_shift_e", methods=["GET", "POST"])
@login_required
def change_shift_e():
    """ask for taking shift or take over shift"""
    return apology("TODO")


@bp.route("/comfirm_schedule", methods=["GET", "POST"])
@login_required
def comfirm_schedule():
    """to comfirm the schedual, which has time limit (after 3 days the schedual publish)"""
    return apology("TODO")