# open world_map file from computer to see map

from src.visualiser import create_map, add_marker
from src.api import fetch_flights

#create a map and add a marker
world_map = create_map([20,20])
add_marker(world_map, 20, 20, "Test Plane")
world_map.save("world_map.html")

AIRPORT_ICAO = "EDDF"
TIME_RANGE = 36000
fetch_flights(AIRPORT_ICAO, TIME_RANGE)


