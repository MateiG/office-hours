import csv
import os

from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "you-will-never-guess")

from app import constants, utils

users = utils.load_users(path="data/CS188_Fall_2024_roster.csv")


@app.context_processor
def inject_info():
    return dict(
        ticket_count=len(utils.get_tickets(["waiting", "in progress"])),
        queue_status=utils.get_queue_status(),
        zoom_link=constants.ZOOM_LINK,
    )


from app import routes
