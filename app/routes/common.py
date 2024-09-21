from flask import flash, redirect, request, session, url_for

from app import app, utils
from app.constants import users


@app.route("/delete_ticket", methods=["POST"])
def delete_ticket():
    if "user" not in session:
        return redirect(url_for("index"))

    ticket_id = request.form.get("ticket_id")
    email = session["user"]["email"]
    is_admin = users[email]["role"] == "admin"

    ticket = utils.get_ticket(ticket_id)

    if ticket["email"] == email or is_admin:
        utils.delete_ticket(ticket_id)
        flash("Ticket deleted successfully!")
    else:
        flash("You don't have permission to delete this ticket.")

    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    clear_session()
    return redirect(url_for("index"))


def clear_session():
    session.pop("auth", None)
    session.pop("user", None)
