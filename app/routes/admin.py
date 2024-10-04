import json
import os

from flask import flash, redirect, render_template, request, session, url_for

from app import app, constants, users, utils


@app.route("/admin")
def admin_page():
    in_progress_tickets = utils.get_tickets(["in progress"])
    waiting_tickets = utils.get_tickets(["waiting"])
    resolved_tickets = utils.get_tickets(["resolved"], sort_key="time_resolved")[:5]
    return render_template(
        "admin.html",
        name=users[session["user"]["email"]]["name"],
        in_progress_tickets=in_progress_tickets,
        waiting_tickets=waiting_tickets,
        resolved_tickets=resolved_tickets,
    )


@app.route("/admin/open_queue", methods=["POST"])
def open_queue():
    utils.set_queue_status("open")
    flash("Office hours are now open.")
    return redirect(url_for("admin_page"))


@app.route("/admin/close_queue", methods=["POST"])
def close_queue():
    utils.set_queue_status("closed")
    flash("Office hours are now closed.")
    return redirect(url_for("admin_page"))


@app.route("/admin/assign_ticket", methods=["POST"])
def assign_ticket():
    ticket_id = request.form.get("ticket_id")
    admin_email = session["user"]["email"]
    admin_name = users[admin_email]["name"]
    ticket = utils.help_ticket(
        ticket_id,
        admin_email,
        admin_name,
    )

    if ticket["location"].lower() == "online":
        subject = "CS188 Office Hours Ticket Update"
        student_body = f"Your ticket is now being helped by {users[admin_email]['name']} ({admin_email}). \nJoin the Zoom meeting at {constants.ZOOM_LINK}."
        utils.send_email(ticket["email"], subject, student_body)

    flash(f"{ticket["name"]}'s ticket has been assigned to you.")
    return redirect(url_for("admin_page"))


@app.route("/admin/resolve_ticket", methods=["POST"])
def resolve_ticket():
    ticket_id = request.form.get("ticket_id")
    ticket = utils.resolve_ticket(ticket_id)

    ticket_path = os.path.join("data/tickets", f"{ticket_id}.json")
    with open(ticket_path, "w") as f:
        json.dump(ticket, f, indent=4)

    flash(f"{ticket["name"]}'s ticket has been resolved.")
    return redirect(url_for("admin_page"))


@app.route("/admin/unresolve_ticket", methods=["POST"])
def unresolve_ticket():
    ticket_id = request.form.get("ticket_id")
    ticket = utils.unresolve_ticket(ticket_id)

    ticket_path = os.path.join("data/tickets", f"{ticket_id}.json")
    if os.path.exists(ticket_path):
        os.remove(ticket_path)
    
    flash(f"{ticket["name"]}'s ticket has been unresolved.")
    return redirect(url_for("admin_page"))


@app.route("/admin/requeue_ticket", methods=["POST"])
def requeue_ticket():
    ticket_id = request.form.get("ticket_id")
    ticket = utils.unhelp_ticket(ticket_id)

    flash(f"{ticket["name"]}'s ticket has been requeued.")
    return redirect(url_for("admin_page"))
