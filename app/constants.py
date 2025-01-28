import csv
import json
import os

ASSIGNMENTS = (
    [f"Homework {i}" for i in range(1, 11)]
    + [f"Project {i}" for i in range(1, 6)]
    + ["Other"]
)
LOCATIONS = ["Inside Soda 341B", "Outside Soda 341B", "Online"]
ZOOM_LINK = "https://berkeley.zoom.us/j/97522023870"

ROSTER_PATH = "data/CS188SP25_roster.csv"
USERS = {}
if os.path.exists(ROSTER_PATH):
    with open(ROSTER_PATH) as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            name = row[0].strip() + " " + row[1].strip()
            email = row[3].strip().lower()
            role = row[4].strip().lower()
            USERS[email] = {
                "name": name,
                "email": email,
                "role": role,
            }
num_admins = len([user for user in USERS.values() if user["role"] == "admin"])
num_students = len([user for user in USERS.values() if user["role"] == "student"])
print(f"Loaded {num_admins} admins and {num_students} students.")
