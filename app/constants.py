import csv
import json
import os

ASSIGNMENTS = [f"Homework {i}" for i in range(1, 11)] + [
    f"Project {i}" for i in range(1, 6)
]
LOCATIONS = ["Online", "Inside Soda 341B", "Outside Soda 341B"]
ZOOM_LINK = "https://berkeley.zoom.us/j/97522023870"

ROSTER_PATH = "data/CS188_Fall_2024_roster.csv"
