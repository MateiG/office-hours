import csv
import os

from flask import Flask, redirect, request, session, url_for

from app import constants, utils

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "you-will-never-guess")

os.makedirs("data/tickets", exist_ok=True)
users = utils.load_users()


@app.context_processor
def inject_info():
    return dict(
        ticket_count=len(utils.get_tickets(["waiting", "in progress"])),
        queue_status=utils.get_queue_status(),
        zoom_link=constants.ZOOM_LINK,
    )

from app import routes
