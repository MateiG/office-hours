import csv
import os
import traceback

from flask import Flask, jsonify, redirect, render_template, request, session, url_for

from app import constants, utils

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "you-will-never-guess")

users = utils.load_users()
num_admins = len([user for user in users.values() if user["role"] == "admin"])
num_students = len([user for user in users.values() if user["role"] == "student"])
print(f"Loaded {num_admins} admins and {num_students} students.")


@app.context_processor
def inject_info():
    return {
        "queue_status": utils.get_queue_status(),
        "ticket_count": len(utils.get_tickets(["waiting", "in progress"])),
        "zoom_link": constants.ZOOM_LINK,
    }


@app.errorhandler(Exception)
def handle_exception(e):
    print(f"URL: {request.url}")
    print(traceback.format_exc())

    return render_template("error.html", error="An unexpected error occurred"), 500


from app import routes
