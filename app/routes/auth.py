import random
from datetime import datetime, timedelta

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app import utils
from app.constants import USERS
from app.routes.helper import clear_session

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.before_request
def check_auth():
    if "user" in session:
        flash("You are already logged in.")
        return redirect(url_for("main.index"))

    if "auth" not in session:
        flash("Please enter your email to log in.")
        return redirect(url_for("main.index"))


@auth_bp.route("/verify_code", methods=["GET", "POST"])
def verify_code():
    if request.method == "POST":
        expiration_time = session["auth"]["expiration_time"]
        if datetime.now().timestamp() > expiration_time:
            clear_session()
            flash("Your verification code expired, please request another.")
            return redirect(url_for("main.index"))

        entered_code = request.form["code"]
        if entered_code == session["auth"]["code"]:
            email = session["auth"]["email"]
            session["user"] = USERS[email]
            return redirect(url_for("main.index"))
        else:
            flash("Invalid code.")
    return render_template("verify_code.html", email=session["auth"]["email"])


@auth_bp.route("/resend_code", methods=["POST"])
def resend_code():
    auth = session["auth"]
    email = auth["email"]
    auth["code"] = code = str(random.randint(100000, 999999))
    auth["expiration_time"] = expiration_time = datetime.now() + timedelta(minutes=10)

    subject = "CS188 Office Hours Login Code"
    body = f"Your new login code is: {code}\nThis code will expire in 10 minutes."
    utils.send_email(email, subject, body)
    flash("A new code has been sent to your email.")
    return redirect(url_for("auth.verify_code"))


@auth_bp.route("/cancel_verification", methods=["POST"])
def cancel_verification():
    clear_session()
    flash("Verification process cancelled. Please start over if you want to log in.")
    return redirect(url_for("main.index"))
