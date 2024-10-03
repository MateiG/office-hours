import random
from datetime import datetime, timedelta

from flask import flash, redirect, render_template, request, session, url_for

from app import app, users, utils
from app.routes.common import clear_session


@app.before_request
def check_auth():
    if request.path.startswith("/admin"):
        if "user" not in session or session["user"]["role"] != "admin":
            flash("You must be an admin to access that page.")
            return redirect(url_for("index"))
    elif request.path.startswith("/student"):
        if "user" not in session or session["user"]["role"] != "student":
            flash("You must be a student to access that page.")
            return redirect(url_for("index"))


@app.route("/", methods=["GET", "POST"])
def index():
    if "user" in session:
        email = session["user"]["email"]
        if users[email]["role"] == "admin":
            return redirect(url_for("admin_page"))
        else:
            return redirect(url_for("student_page"))

    if "auth" in session:
        return redirect(url_for("verify_code"))

    if request.method == "POST":
        email = request.form["email"].strip().lower()

        if email in users:
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
            return redirect(url_for("verify_code"))
        else:
            flash("Invalid email.")

    ticket_count = len(utils.get_tickets(["waiting", "in progress"]))
    queue_status = utils.get_queue_status()
    return render_template(
        "index.html", ticket_count=ticket_count, queue_status=queue_status
    )


@app.route("/verify_code", methods=["GET", "POST"])
def verify_code():
    if "user" in session:
        return redirect(url_for("index"))

    if "auth" not in session:
        flash("Couldn't find your session information.")
        return redirect(url_for("index"))

    if request.method == "POST":
        expiration_time = session["auth"]["expiration_time"]
        if datetime.now().timestamp() > expiration_time:
            clear_session()
            flash("Your verification code expired, please request another.")
            return redirect(url_for("index"))

        entered_code = request.form["code"]
        if entered_code == session["auth"]["code"]:
            email = session["auth"]["email"]
            session["user"] = users[email]
            return redirect(url_for("index"))
        else:
            flash("Invalid code.")
    return render_template("verify_code.html", email=session["auth"]["email"])


@app.route("/resend_code", methods=["POST"])
def resend_code():
    if "user" in session:
        return redirect(url_for("index"))

    if "auth" not in session:
        flash("Couldn't find your session information.")
        return redirect(url_for("index"))

    auth = session["auth"]
    email = auth["email"]
    auth["code"] = code = str(random.randint(100000, 999999))
    auth["expiration_time"] = expiration_time = datetime.now() + timedelta(minutes=10)

    subject = "CS188 Office Hours Login Code"
    body = f"Your new login code is: {code}\nThis code will expire in 10 minutes."
    utils.send_email(email, subject, body)
    flash("A new code has been sent to your email.")
    return redirect(url_for("verify_code"))


@app.route("/cancel_verification", methods=["POST"])
def cancel_verification():
    if "user" in session:
        return redirect(url_for("index"))

    clear_session()
    flash("Verification process cancelled. Please start over if you want to log in.")
    return redirect(url_for("index"))
