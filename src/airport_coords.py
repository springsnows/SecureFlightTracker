import json

def get_coordinates_airport(airport_code, filename="data/airports.json"):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            airport = data.get(airport_code.upper())
            if airport:
                return airport.get("lat"), airport.get("lon")
            else:
                print(f"ICAO code '{airport_code}' not found.")
                return None, None
    except FileNotFoundError:
        print("Airport data file not found.")
        return None, None

coords = get_coordinates_airport("EDDF")
print(f"Coordinates for EDDF: {coords}")
