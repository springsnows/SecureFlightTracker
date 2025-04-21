import requests
import time
from datetime import datetime

# testing fetching all active data and then filtering by airport
# airport = "EGLL"  # Heathrow
# response = requests.get(f"https://www.airport-data.com/api/ap_info.json?icao={airport}")
# can't request this much data

# set airport code
# EDDF for Frankfurt
DEFAULT_AIRPORT_ICAO = "EDDF" # default airport

# setting time range for requests
DEFAULT_TIME_RANGE = 10800 # 3 hours


# function to fetch all flights from selected airport
def fetch_flights(AIRPORT_ICAO, TIME_RANGE):
    # use provided airport_icao, default to EDDF if None
    current_airport = AIRPORT_ICAO if AIRPORT_ICAO else DEFAULT_AIRPORT_ICAO
    
    # set time range
    end_time = int(time.time())
    begin_time = end_time - TIME_RANGE

    departures_list = []
    arrivals_list = []
    error_message = None

    # fetch all departures
    try:
        dep_response = requests.get(f"https://opensky-network.org/api/flights/departure?airport={current_airport}&begin={begin_time}&end={end_time}")
        dep_response.raise_for_status() # Check for HTTP errors
        departures_data = dep_response.json()

        if departures_data:
            for flight in departures_data:
                # convert UNIX time
                firstseen_time = flight.get('firstSeen')
                if firstseen_time:
                    firstTime = datetime.utcfromtimestamp(firstseen_time).strftime('%H:%M') # Simplified time format
                    dest_airport = flight.get('estArrivalAirport', 'N/A')
                    departures_list.append(f"{flight['icao24']} → {dest_airport} ({firstTime})")
    except requests.exceptions.RequestException as e:
        error_message = f"Error fetching departures: {e}"
        print(error_message) # Keep server-side logging
    except Exception as e:
        error_message = f"Error processing departures: {e}"
        print(error_message)

    # fetch all arrivals
    try:
        arrival_response = requests.get(f"https://opensky-network.org/api/flights/arrival?airport={current_airport}&begin={begin_time}&end={end_time}")
        arrival_response.raise_for_status()
        arrivals_data = arrival_response.json()

        if arrivals_data:
            for flight in arrivals_data:
                lastseen_time = flight.get('lastSeen')
                if lastseen_time:
                    lastTime = datetime.utcfromtimestamp(lastseen_time).strftime('%H:%M') # Simplified time format
                    orig_airport = flight.get('estDepartureAirport', 'N/A')
                    arrivals_list.append(f"{flight['icao24']} ← {orig_airport} ({lastTime})")
    except requests.exceptions.RequestException as e:
        err_msg = f"Error fetching arrivals: {e}"
        print(err_msg)
        if error_message: error_message += f"; {err_msg}"
        else: error_message = err_msg
    except Exception as e:
        err_msg = f"Error processing arrivals: {e}"
        print(err_msg)
        if error_message: error_message += f"; {err_msg}"
        else: error_message = err_msg

    return {
        "departures": departures_list,
        "arrivals": arrivals_list,
        "error": error_message
    }

# def log_flight_info(flight):
#     with open(LOG_FILE, "a")

# def select_and_log_flight(AIRPORT_ICAO):