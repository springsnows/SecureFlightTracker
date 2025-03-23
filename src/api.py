import requests

OPENSKY_URL = "https://opensky-network.org/api/states/all"

def fetch_flights():
    response = requests.get(OPENSKY_URL)
    if response.status_code == 200:
        return response.json()
    return None

if __name__ == "__main__":
    flights = fetch_flights()
    print(flights)  # Debugging
