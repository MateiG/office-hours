import json
import os

from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)

from app import utils
from app.constants import USERS, ZOOM_LINK

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.before_request
def check_admin_auth():
    if "user" not in session or session["user"]["role"] != "admin":
        flash("You must be an admin to access that page.")
        return redirect(url_for("main.index"))

@admin_bp.route("/")
def index():
    in_progress_tickets = utils.get_tickets(["in progress"])
    waiting_tickets = utils.get_tickets(["waiting"])
    resolved_tickets = utils.get_tickets(["resolved"], sort_key="time_resolved", reverse=True)[:5]
    return render_template(
        "admin.html",
        name=USERS[session["user"]["email"]]["name"],
        in_progress_tickets=in_progress_tickets,
        waiting_tickets=waiting_tickets,
        resolved_tickets=resolved_tickets,
    )


@admin_bp.route("/open_queue", methods=["POST"])
def open_queue():
    utils.set_queue_status("open")
    flash("Office hours are now open.")
    return redirect(url_for("admin.index"))


@admin_bp.route("/close_queue", methods=["POST"])
def close_queue():
    utils.set_queue_status("closed")
    flash("Office hours are now closed.")
    return redirect(url_for("admin.index"))


@admin_bp.route("/assign_ticket", methods=["POST"])
def assign_ticket():
    ticket_id = request.form.get("ticket_id")
    admin_email = session["user"]["email"]
    admin_name = USERS[admin_email]["name"]
    ticket = utils.help_ticket(
        ticket_id,
        admin_email,
        admin_name,
    )
    if not ticket:
        flash("Ticket not found. It may have been deleted.")
        return redirect(url_for("admin.index"))

    if ticket["location"].lower() == "online":
        subject = "CS188 Office Hours Ticket Update"
        student_body = f"Your ticket is now being helped by {USERS[admin_email]['name']} ({admin_email}). \nJoin the Zoom meeting at {ZOOM_LINK}."
        utils.send_email(ticket["email"], subject, student_body)

    flash(f"{ticket['name']}'s ticket has been assigned to you.")
    return redirect(url_for("admin.index"))


@admin_bp.route("/resolve_ticket", methods=["POST"])
def resolve_ticket():
    ticket_id = request.form.get("ticket_id")
    ticket = utils.resolve_ticket(ticket_id)
    if not ticket:
        flash("Ticket not found. It may have been deleted.")
        return redirect(url_for("admin.index"))

    ticket_path = os.path.join("data/tickets", f"{ticket_id}.json")
    with open(ticket_path, "w") as f:
        json.dump(ticket, f, indent=4)

    flash(f"{ticket['name']}'s ticket has been resolved.")
    return redirect(url_for("admin.index"))


@admin_bp.route("/unresolve_ticket", methods=["POST"])
def unresolve_ticket():
    ticket_id = request.form.get("ticket_id")
    ticket = utils.unresolve_ticket(ticket_id)
    if not ticket:
        flash("Ticket not found. It may have been deleted.")
        return redirect(url_for("admin.index"))


    ticket_path = os.path.join("data/tickets", f"{ticket_id}.json")
    if os.path.exists(ticket_path):
        os.remove(ticket_path)
    
    flash(f"{ticket['name']}'s ticket has been unresolved.")
    return redirect(url_for("admin.index"))


@admin_bp.route("/requeue_ticket", methods=["POST"])
def requeue_ticket():
    ticket_id = request.form.get("ticket_id")
    ticket = utils.unhelp_ticket(ticket_id)
    if not ticket:
        flash("Ticket not found. It may have been deleted.")
        return redirect(url_for("admin.index"))

    flash(f"{ticket['name']}'s ticket has been requeued.")
    return redirect(url_for("admin.index"))

@admin_bp.route("/delete_ticket", methods=["POST"])
def delete_ticket():
    ticket_id = request.form.get("ticket_id")
    ticket = utils.get_ticket(ticket_id)

    utils.delete_ticket(ticket_id)
    flash(f"{ticket['name']}'s ticket has been deleted.")
    return redirect(url_for("admin.index"))
