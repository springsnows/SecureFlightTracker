# This file is kept for reference. The main application now runs through app.py
# To run the application, use: uvicorn app:app --reload

from src.visualiser import create_map
from src.api import fetch_flights
from src.tracker import flight_details, get_coordinates

# Create initial map
world_map = create_map([50,10])
world_map.save("world_map.html")

# Constants for reference
AIRPORT_ICAO = "EDDF"
ICAO24_CODE = "3c64aa"
