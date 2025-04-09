import requests
import time

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
            return flight_info
        else:
            return{"Error": "No valid position found."}
    else:
        return {"Error": f"Request failed status code {response.status_code}"}

icao24_code = "3c66b4"

# info = flight_details(icao24_code)
# print(info)

while True:
    info = flight_details(icao24_code)
    print(info)
    print("Refreshing details every 1 minutes")
    time.sleep(60)