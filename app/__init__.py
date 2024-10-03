import csv
import os

from flask import Flask, redirect, request, session, url_for

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "you-will-never-guess")


@app.before_request
def check_auth():
    if request.path.startswith("/admin"):
        if "user" not in session or session["user"]["role"] != "admin":
            return redirect(url_for("index"))
    elif request.path.startswith("/student"):
        if "user" not in session or session["user"]["role"] != "student":
            return redirect(url_for("index"))


@app.context_processor
def inject_info():
    return dict(
        ticket_count=len(utils.get_tickets(["waiting", "in progress"])),
        queue_status=utils.get_queue_status(),
        zoom_link=constants.ZOOM_LINK,
    )


from app import constants, utils

users = utils.load_users()

from app import routes
