import csv
import json
import os

ASSIGNMENTS = [f"Homework {i}" for i in range(1, 11)] + [
    f"Project {i}" for i in range(1, 6)
]
LOCATIONS = ["Online", "Inside Soda 341B", "Outside Soda 341B"]
ZOOM_LINK = "http://google.com"
