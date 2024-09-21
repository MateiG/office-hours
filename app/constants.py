import csv
import json

ASSIGNMENTS = [f"Homework {i}" for i in range(1, 11)] + [
    f"Project {i}" for i in range(1, 6)
]
LOCATIONS = ["Online", "Inside Soda 341B", "Outside Soda 341B"]
ZOOM_LINK = "http://google.com"

users = {}
with open("data/users.csv") as f:
    reader = csv.reader(f)
    for row in reader:
        users[row[0]] = {
            "email": row[0].strip().lower(),
            "name": row[1].strip(),
            "role": row[2].strip().lower(),
        }
