import json
import os


def load_data(filename):
    if not os.path.exists(filename):
        print(f"{filename} not found")
        return []

    with open(filename, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []


def save_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file)
