from flask import flash, redirect, request, session, url_for

from app import app, users, utils


@app.route("/delete_ticket", methods=["POST"])
def delete_ticket():
    if "user" not in session:
        return redirect(url_for("index"))

    ticket_id = request.form.get("ticket_id")
    current_email = session["user"]["email"]
    is_admin = users[current_email]["role"] == "admin"

    ticket = utils.get_ticket(ticket_id)

    if ticket["email"] == current_email:
        utils.delete_ticket(ticket_id)
        flash("Your ticket has been deleted.")
    elif is_admin:
        utils.delete_ticket(ticket_id)
        flash(f"{ticket['name']}'s ticket has been deleted.")
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
