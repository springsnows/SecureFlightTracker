from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.api import fetch_flights, TIME_RANGE
from src.tracker import flight_details, get_coordinates, save_to_json, JSON_FILE
from src.visualiser import plane_marker, create_map
import asyncio
import json
import time
from datetime import datetime

app = FastAPI()

# enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Active WebSocket connections
active_connections = set()

@app.get("/flights/{airport_icao}")
async def get_flights_for_airport(airport_icao: str):
    """API endpoint to get flights for a given airport."""
    try:
        # Call fetch_flights which now returns the combined flight data
        all_flights = fetch_flights(airport_icao, TIME_RANGE)
        
        # Format flight data for the frontend
        flight_list = []
        
        # Parse the flight data to create flight info strings
        for flight in all_flights:
            flight_type = "departure" if "firstSeen" in flight else "arrival"
            
            if flight_type == "departure":
                time_str = datetime.utcfromtimestamp(flight['firstSeen']).strftime('%Y-%m-%d %H:%M:%S')
                info = f"Flight {flight['icao24']} → {flight['estArrivalAirport']}, Departure: {time_str}"
            else:
                time_str = datetime.utcfromtimestamp(flight['lastSeen']).strftime('%Y-%m-%d %H:%M:%S')
                info = f"Flight {flight['icao24']} from {flight['estDepartureAirport']}, Arrival: {time_str}"
                
            flight_list.append({
                "icao24": flight['icao24'],
                "info": info
            })
            
        return {"flights": flight_list}
    except Exception as e:
        print(f"Error fetching flights for {airport_icao}: {e}")
        return {"error": str(e)}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.add(websocket)
    
    print(f"WebSocket connected: {websocket.client}")
    current_icao24 = None
    
    try:
        # Main loop to receive messages
        while True:
            try:
                # Wait for messages from client
                message = await websocket.receive_json()
                action = message.get("action")
                icao24 = message.get("icao24")
                
                if action == "track" and icao24:
                    print(f"Tracking flight {icao24}")
                    current_icao24 = icao24
                    
                    # Initial fetch
                    info = flight_details(icao24)
                    latitude, longitude = get_coordinates()
                    
                    # Send initial data regardless of errors
                    await websocket.send_json({
                        "flight_info": info,
                        "coordinates": {
                            "latitude": latitude,
                            "longitude": longitude
                        }
                    })
                    
                    # Start updates every 30 seconds
                    for _ in range(60):  # Keep updating for 30 minutes max
                        # Wait 30 seconds between updates
                        await asyncio.sleep(30)
                        
                        # Exit if disconnected
                        if websocket not in active_connections:
                            break
                            
                        # Get updated data regardless of errors
                        info = flight_details(icao24)
                        latitude, longitude = get_coordinates()
                        
                        # Always send even if there's an error
                        await websocket.send_json({
                            "flight_info": info,
                            "coordinates": {
                                "latitude": latitude,
                                "longitude": longitude
                            }
                        })
                        
            except Exception as e:
                print(f"Error in WebSocket handler: {e}")
                await asyncio.sleep(1)
                    
    except WebSocketDisconnect:
        print(f"WebSocket disconnected: {websocket.client}")
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        # Remove from active connections
        active_connections.discard(websocket)

# Mount static files
app.mount("/", StaticFiles(directory=".", html=True), name="static")
