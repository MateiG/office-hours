import os

from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "you-will-never-guess")

from app import routes
from app import utils
from app import constants


@app.context_processor
def inject_info():
    return dict(
        ticket_count=len(utils.get_tickets(["waiting", "in progress"])),
        queue_status=utils.get_queue_status(),
        zoom_link=constants.ZOOM_LINK,
    )
