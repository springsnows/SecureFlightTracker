from fastapi import FastAPI, WebSocket, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from src.api import fetch_flights
from src.tracker import flight_details, get_coordinates
import asyncio
import json

app = FastAPI()

# enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# store active websocket connections
active_connections = set()

# Placeholder variables for coordinates - WILL BE REPLACED LATER
# Airport coordinates
AIRPORT_LAT = 50.026421
AIRPORT_LONG = 8.543125

# Plane coordinates
PLANE_LAT = 50.0016
PLANE_LONG = 8.3464

# flight to track - will be replaced by user input later
ICAO24_CODE = "44ce79"

# serve world_map.html with template variables
@app.get("/")
async def root():
    # Read the HTML file
    with open("world_map.html", "r") as file:
        html_content = file.read()
    
    # Replace placeholder variables with actual values
    html_content = html_content.replace("{{ Latitude }}", str(PLANE_LAT))
    html_content = html_content.replace("{{ Longitude }}", str(PLANE_LONG))
    html_content = html_content.replace("{{ AirportLat }}", str(AIRPORT_LAT))
    html_content = html_content.replace("{{ AirportLong }}", str(AIRPORT_LONG))
    
    return HTMLResponse(html_content)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.add(websocket)
    try:
        while True:
            # fetch flight data
            info = flight_details(ICAO24_CODE)
            latitude, longitude = get_coordinates()
            
            # prepare data to send
            data = {
                "flight_info": info,
                "coordinates": {
                    "latitude": latitude,
                    "longitude": longitude
                }
            }
            
            # send to all connected clients
            for connection in active_connections:
                await connection.send_json(data)
            
            # wait before next update
            await asyncio.sleep(10)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        active_connections.remove(websocket)

# Mount static files
app.mount("/static", StaticFiles(directory="."), name="static")
