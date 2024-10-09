import csv
import json
import os
import smtplib
import uuid
from datetime import datetime, timedelta
from email.mime.text import MIMEText

from dotenv import load_dotenv
from redis import Redis

from app import constants

redis_client = Redis(host="localhost", port=6379, db=0, decode_responses=True)

load_dotenv()
sender_email = os.getenv("SENDER_EMAIL")
sender_password = os.getenv("SENDER_PASSWORD")


def send_email(to_email, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())


def set_queue_status(status):
    redis_client.set("queue_status", status)


def get_queue_status():
    status = redis_client.get("queue_status")
    return status if status else "closed"


def create_ticket(name, email, location, assignment, description):
    ticket = {
        "name": name,
        "email": email,
        "location": location,
        "assignment": assignment,
        "description": description,
        "status": "waiting",
        "helped_by": "",
        "helped_by_name": "",
        "time_created": datetime.now().isoformat(),
        "time_helped": "",
        "time_resolved": "",
    }

    ticket_id = str(uuid.uuid4())
    ticket["id"] = ticket_id
    redis_client.set(f"ticket:{ticket_id}", json.dumps(ticket))
    return ticket


def get_ticket(id):
    ticket = redis_client.get(f"ticket:{id}")
    if not ticket:
        return None

    ticket = json.loads(ticket)
    time_diff = datetime.now() - datetime.fromisoformat(ticket["time_created"])
    if time_diff < timedelta(minutes=1):
        ticket["time_ago"] = f"{time_diff.seconds} seconds ago"
    elif time_diff < timedelta(hours=1):
        ticket["time_ago"] = f"{time_diff.seconds // 60} minutes ago"
    elif time_diff < timedelta(days=1):
        ticket["time_ago"] = f"{time_diff.seconds // 3600} hours ago"
    else:
        ticket["time_ago"] = f"{time_diff.days} days ago"

    return ticket


def get_tickets(status_list: list, sort_key="time_created", reverse=False):
    tickets = []
    for key in redis_client.scan_iter(match="ticket:*"):
        ticket = get_ticket(key.split(":")[1])
        if not ticket:
            continue
        if ticket["status"] in status_list:
            tickets.append(ticket)
    tickets.sort(key=lambda x: x[sort_key], reverse=reverse)
    return tickets


def help_ticket(ticket_id, email, name):
    ticket = get_ticket(ticket_id)
    if not ticket:
        return None
    ticket["status"] = "in progress"
    ticket["helped_by"] = email
    ticket["helped_by_name"] = name
    ticket["time_helped"] = datetime.now().isoformat()
    redis_client.set(f"ticket:{ticket_id}", json.dumps(ticket))
    return ticket


def unhelp_ticket(ticket_id):
    ticket = get_ticket(ticket_id)
    if not ticket:
        return None
    ticket["status"] = "waiting"
    ticket["helped_by"] = ""
    ticket["helped_by_name"] = ""
    ticket["time_helped"] = ""
    redis_client.set(f"ticket:{ticket_id}", json.dumps(ticket))
    return ticket


def resolve_ticket(ticket_id):
    ticket = get_ticket(ticket_id)
    if not ticket:
        return None
    ticket["status"] = "resolved"
    ticket["time_resolved"] = datetime.now().isoformat()
    redis_client.set(f"ticket:{ticket_id}", json.dumps(ticket))
    return ticket


def unresolve_ticket(ticket_id):
    ticket = get_ticket(ticket_id)
    if not ticket:
        return None
    ticket["status"] = "in progress"
    ticket["time_resolved"] = ""
    redis_client.set(f"ticket:{ticket_id}", json.dumps(ticket))
    return ticket


def delete_ticket(ticket_id):
    redis_client.delete(f"ticket:{ticket_id}")


def load_users():
    users = {}
    if os.path.exists(constants.ROSTER_PATH):
        with open(constants.ROSTER_PATH) as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                name = row[0].strip() + " " + row[1].strip()
                email = row[3].strip().lower()
                role = row[4].strip().lower()
                users[email] = {
                    "name": name,
                    "email": email,
                    "role": role,
                }
    return users
