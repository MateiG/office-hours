import csv
import os
import traceback

from flask import (Flask, jsonify, redirect, render_template, request, session,
                   url_for)

from app import constants, utils

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "you-will-never-guess")

os.makedirs("data/tickets", exist_ok=True)
users = utils.load_users()


@app.context_processor
def inject_info():
    return {
        "queue_status": utils.get_queue_status(),
        "ticket_count": len(utils.get_tickets(["waiting", "in progress"])),
        "zoom_link": constants.ZOOM_LINK,
    }


@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(traceback.format_exc())

    return render_template("error.html", error="An unexpected error occurred"), 500


from app import routes
