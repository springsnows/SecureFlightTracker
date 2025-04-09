import requests
import time
import os
import json

#links to json file
JSON_FILE = "data/flight_status.json"

def flight_details(ICAO24):
    flight_data = f"https://opensky-network.org/api/tracks/all?icao24={ICAO24}&time=0"
    response = requests.get(flight_data)

    if response.status_code == 200:
        data = response.json()

        if 'icao24' in data and 'path' in data and data['path']:
            last_position = data['path'][-1]

            flight_info = {
                "icao24": data['icao24'],
                "Latitude": last_position[1],
                "Longitude": last_position[2],
                "Baro_Altitude": last_position[3],
                "Grounded": last_position[5]
            }

            save_to_json(JSON_FILE, flight_info)
            return flight_info
        else:
            return{"Error": "No valid position found."}
    else:
        return {"Error": f"Request failed status code {response.status_code}"}

icao24_code = "3c6637"

# info = flight_details(icao24_code)
# print(info)

def save_to_json(filename, data):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def read_flight_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {"Error": "File not found"}

def get_coordinates(filename="data/flight_status.json"):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            latitude = data.get("Latitude")
            longitude = data.get("Longitude")
            return latitude, longitude
    except FileNotFoundError:
        print("Flight data file not found.")
        return None, None