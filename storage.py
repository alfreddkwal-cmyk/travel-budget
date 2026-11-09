"""JSON persistence for travel plans."""
import json
from pathlib import Path
from budget import TravelBudget


def save_trip(trip, filename="trip.json"):
    path = Path(filename)
    with path.open("w", encoding="utf-8") as file:
        json.dump(trip.to_dict(), file, indent=4)
    return path


def load_trip(filename="trip.json"):
    path = Path(filename)
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    return TravelBudget.from_dict(data)
