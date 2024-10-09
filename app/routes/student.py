from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app import utils
from app.constants import ASSIGNMENTS, LOCATIONS, USERS

student_bp = Blueprint("student", __name__, url_prefix="/student")


@student_bp.before_request
def check_student_auth():
    if "user" not in session or session["user"]["role"] != "student":
        flash("You must be a student to access that page.")
        return redirect(url_for("main.index"))


@student_bp.route("/", methods=["GET", "POST"])
def index():
    email = session["user"]["email"]
    user_ticket = None
    for ticket in utils.get_tickets(["waiting", "in progress"]):
        if ticket["email"] == email:
            user_ticket = ticket
            break

    num_in_queue = 1
    if user_ticket:
        for ticket in utils.get_tickets(["waiting", "in progress"]):
            if ticket["time_created"] < user_ticket["time_created"]:
                num_in_queue += 1

    if request.method == "POST":
        queue_status = utils.get_queue_status()
        if user_ticket or queue_status == "closed":
            flash("You cannot create a new ticket at this time.")
            return redirect(url_for("student.index"))
        else:
            utils.create_ticket(
                USERS[email]["name"],
                email,
                request.form["location"],
                request.form["assignment"],
                request.form["description"],
            )
            flash("Ticket created successfully!")
        return redirect(url_for("student.index"))

    return render_template(
        "student.html",
        name=USERS[session["user"]["email"]]["name"],
        user_ticket=user_ticket,
        assignments=ASSIGNMENTS,
        locations=LOCATIONS,
        num_in_queue=num_in_queue,
    )


@student_bp.route("/delete_ticket", methods=["POST"])
def delete_ticket():
    ticket_id = request.form.get("ticket_id")
    current_email = session["user"]["email"]

    ticket = utils.get_ticket(ticket_id)
    if ticket["email"] == current_email:
        utils.delete_ticket(ticket_id)
        flash("Your ticket has been deleted.")
    else:
        flash("You don't have permission to delete this ticket.")

    return redirect(url_for("student.index"))
