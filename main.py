# open world_map file from computer to see map
import time
from src.visualiser import create_map, add_marker, plane_marker
from src.api import fetch_flights
from src.tracker import flight_details, get_coordinates

#create a map and add a marker
world_map = create_map([50,10])
add_marker(world_map, 50.033333, 8.570556, "Frankfurt Airport")
plane_marker(world_map, 48.782, 11.5294, "Test Plane")
world_map.save("world_map.html")

AIRPORT_ICAO = "EDDF"
# TIME_RANGE = 36000
# fetch_flights(AIRPORT_ICAO, TIME_RANGE)

ICAO24_CODE = "3c6637"

# while True:
#     info = flight_details(ICAO24_CODE)
#     add_marker(world_map, 50.033333, 8.570556, "Frankfurt Airport")
#     latitude, longitude = get_coordinates()
#     plane_marker(world_map, latitude, longitude, "Test Plane")
#     world_map.save("world_map.html")
#     time.sleep(10)
