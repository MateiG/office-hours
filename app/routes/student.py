from flask import flash, redirect, render_template, request, session, url_for

from app import app, users, utils
from app.constants import ASSIGNMENTS, LOCATIONS


@app.route("/student", methods=["GET", "POST"])
def student_page():
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
            return redirect(url_for("student_page"))
        else:
            utils.create_ticket(
                users[email]["name"],
                email,
                request.form["location"],
                request.form["assignment"],
                request.form["description"],
            )
            flash("Ticket created successfully!")
        return redirect(url_for("student_page"))

    return render_template(
        "student.html",
        name=users[session["user"]["email"]]["name"],
        user_ticket=user_ticket,
        assignments=ASSIGNMENTS,
        locations=LOCATIONS,
        num_in_queue=num_in_queue,
    )
