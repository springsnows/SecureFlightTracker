#main.py
# from src.visualiser import add_marker, create_map
from src.api import fetch_flights

# #create a map and add a marker
# add_marker(world_map, 20, 20, "Test Plane")
# world_map.save("world_map.html")

AIRPORT_ICAO = "EDDF"
TIME_RANGE = 36000
fetch_flights(AIRPORT_ICAO, TIME_RANGE)


