import requests
import time
from datetime import datetime

# testing fetching all active data and then filtering by airport
# airport = "EGLL"  # Heathrow
# response = requests.get(f"https://www.airport-data.com/api/ap_info.json?icao={airport}")
# can't request this much data

# set airport code 
# EGLL for Heathrow
AIRPORT_ICAO = "EGLL"

# setting 1 hour range for requests
end_time = int(time.time())
begin_time = end_time - 13800


departures = []
arrivals = []
#Opensky API
dep_url = f"https://opensky-network.org/api/flights/departure?airport={AIRPORT_ICAO}&begin={begin_time}&end={end_time}"
arrival_url = f"https://opensky-network.org/api/flights/arrival?airport={AIRPORT_ICAO}&begin={begin_time}&end={end_time}"

dep_response = requests.get(dep_url)
#200 is HTTPS response code for success
if dep_response.status_code == 200:
    departures = dep_response.json()

    if departures:
        print("\nDepartures from", AIRPORT_ICAO)
        for flight in departures:
            # convert UNIX time
            firstseen_time = flight['firstSeen']
            firstTime = datetime.utcfromtimestamp(firstseen_time).strftime('%Y-%m-%d %H:%M:%S')
            print(f"Flight {flight['icao24']} → {flight['estArrivalAirport']}, Departure: {firstTime}")
    else:
        print("Error fetching departure:", dep_response.status_code)

arrival_response = requests.get(arrival_url)
if arrival_response.status_code == 200:
    arrivals = arrival_response.json()

    if arrivals:
         print("\nArrivals at", AIRPORT_ICAO)
         for flight in arrivals:
            lastseen_time = flight['lastSeen']
            lastTime = datetime.utcfromtimestamp(lastseen_time).strftime('%Y-%m-%d %H:%M:%S')
            print(f"Flight {flight['icao24']} from {flight['estDepartureAirport']}, Arrival: {lastTime}")
    else:
        print("Error fetching arrivals:", arrival_response.status_code)