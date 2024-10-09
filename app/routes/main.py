import random
from datetime import datetime, timedelta

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app import utils
from app.constants import USERS
from app.routes.helper import clear_session

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET", "POST"])
def index():
    if "user" in session:
        email = session["user"]["email"]
        if USERS[email]["role"] == "admin":
            return redirect(url_for("admin.index"))
        else:
            return redirect(url_for("student.index"))

    if "auth" in session:
        return redirect(url_for("auth.verify_code"))

    if request.method == "POST":
        email = request.form["email"].strip().lower()

        if email in USERS:
            code = str(random.randint(100000, 999999))
            expiration_time = datetime.now() + timedelta(minutes=10)
            auth = {
                "code": code,
                "expiration_time": expiration_time.timestamp(),
                "email": email,
            }
            session["auth"] = auth

            subject = "CS188 Office Hours Login Code"
            body = f"Your login code is: {code}\nThis code will expire in 10 minutes."
            utils.send_email(email, subject, body)
            return redirect(url_for("auth.verify_code"))
        else:
            flash("Invalid email.")

    return render_template("login.html")


@main_bp.route("/logout")
def logout():
    clear_session()
    return redirect(url_for("main.index"))
