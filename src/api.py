import requests
import time
from datetime import datetime

# testing fetching all active data and then filtering by airport
# airport = "EGLL"  # Heathrow
# response = requests.get(f"https://www.airport-data.com/api/ap_info.json?icao={airport}")
# can't request this much data

# set airport code 
# EDDF for Frankfurt
AIRPORT_ICAO = "EDDF"

# setting time range for requests
time_range = 13800


departures = []
arrivals = []


#function to set time range


#function to fetch all flights from selected airport
def fetch_flights(AIRPORT_ICAO,TIME_RANGE):

    #set time range
    end_time = int(time.time())
    begin_time = end_time - TIME_RANGE

    #fetch all departures
    dep_response = requests.get(f"https://opensky-network.org/api/flights/departure?airport={AIRPORT_ICAO}&begin={begin_time}&end={end_time}")
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

    #fetch all arrivals
    arrival_response = requests.get(f"https://opensky-network.org/api/flights/arrival?airport={AIRPORT_ICAO}&begin={begin_time}&end={end_time}")
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

# def log_flight_info(flight):
#     with open(LOG_FILE, "a")

# def select_and_log_flight(AIRPORT_ICAO):