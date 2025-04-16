from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.api import fetch_flights
from src.tracker import flight_details, get_coordinates
import asyncio
import json

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active WebSocket connections
active_connections = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.add(websocket)
    try:
        while True:
            # Fetch flight data
            ICAO24_CODE = "3c64aa"
            info = flight_details(ICAO24_CODE)
            latitude, longitude = get_coordinates()
            
            # Prepare data to send
            data = {
                "flight_info": info,
                "coordinates": {
                    "latitude": latitude,
                    "longitude": longitude
                }
            }
            
            # Send to all connected clients
            for connection in active_connections:
                await connection.send_json(data)
            
            # Wait before next update
            await asyncio.sleep(10)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        active_connections.remove(websocket)

# Mount static files
app.mount("/", StaticFiles(directory=".", html=True), name="static")
