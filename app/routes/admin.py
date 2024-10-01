import json
import os
from datetime import datetime

from flask import flash, redirect, render_template, request, session, url_for

from app import app, users, utils, constants


@app.route("/admin")
def admin_page():
    if "user" not in session or session["user"]["role"] != "admin":
        return redirect(url_for("index"))

    in_progress_tickets = utils.get_tickets(["in progress"])
    waiting_tickets = utils.get_tickets(["waiting"])
    return render_template(
        "admin.html",
        name=users[session["user"]["email"]]["name"],
        in_progress_tickets=in_progress_tickets,
        waiting_tickets=waiting_tickets,
    )


@app.route("/admin/open_queue", methods=["POST"])
def open_queue():
    if "user" not in session or session["user"]["role"] != "admin":
        return redirect(url_for("index"))

    utils.set_queue_status("open")
    flash("Office hours are now open.")
    return redirect(url_for("admin_page"))


@app.route("/admin/close_queue", methods=["POST"])
def close_queue():
    if "user" not in session or session["user"]["role"] != "admin":
        return redirect(url_for("index"))

    utils.set_queue_status("closed")
    flash("Office hours are now closed.")
    return redirect(url_for("admin_page"))


@app.route("/admin/assign_ticket", methods=["POST"])
def assign_ticket():
    if "user" not in session or session["user"]["role"] != "admin":
        return redirect(url_for("index"))

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

    return redirect(url_for("admin_page"))


@app.route("/admin/resolve_ticket", methods=["POST"])
def resolve_ticket():
    if "user" not in session or session["user"]["role"] != "admin":
        return redirect(url_for("index"))

    ticket_id = request.form.get("ticket_id")
    ticket = utils.resolve_ticket(ticket_id)

    os.makedirs("data/tickets", exist_ok=True)
    ticket_path = os.path.join("data/tickets", f"{ticket_id}.json")
    with open(ticket_path, "w") as f:
        json.dump(ticket, f, indent=4)
    return redirect(url_for("admin_page"))


@app.route("/admin/requeue_ticket", methods=["POST"])
def requeue_ticket():
    if "user" not in session or session["user"]["role"] != "admin":
        return redirect(url_for("index"))

    ticket_id = request.form.get("ticket_id")
    ticket = utils.unhelp_ticket(ticket_id)
    return redirect(url_for("admin_page"))


@app.route("/admin/reload_roster", methods=["GET"])
def reload_roster():
    if "user" not in session or session["user"]["role"] != "admin":
        return redirect(url_for("index"))

    users = utils.load_users()
    flash("Roster reloaded.")
    return redirect(url_for("admin_page"))
