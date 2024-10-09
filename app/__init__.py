import os
import traceback

from flask import Flask, render_template, request

from app import utils
from app.constants import ZOOM_LINK
from app.routes import admin_bp, auth_bp, main_bp, student_bp


def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "you-will-never-guess")

    @app.context_processor
    def inject_info():
        return {
            "queue_status": utils.get_queue_status(),
            "ticket_count": len(utils.get_tickets(["waiting", "in progress"])),
            "zoom_link": ZOOM_LINK,
        }

    @app.errorhandler(Exception)
    def handle_exception(e):
        print(f"URL: {request.url}")
        print(traceback.format_exc())
        return render_template("error.html", error="An unexpected error occurred"), 500

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(student_bp)

    return app
