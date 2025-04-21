from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from src.api import fetch_flights
from src.tracker import flight_details
from src.airport_coords import get_coordinates_airport
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

# --- Constants ---
DEFAULT_TIME_RANGE_SECONDS = 10800 # 3 hours

# --- Global State ---
# default airport: Frankfurt (EDDF)
default_airport_icao = "EDDF"
default_airport_lat, default_airport_lon = get_coordinates_airport(default_airport_icao)

# store current state
current_state = {
    "airport_icao": default_airport_icao,
    "airport_lat": default_airport_lat if default_airport_lat else 50.0333, # fallback coords
    "airport_lon": default_airport_lon if default_airport_lon else 8.5705,
    "tracked_icao24": None, # initially track nothing
}

# serve world_map.html with initial airport coordinates
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # read the HTML file
    # Explicitly specify UTF-8 encoding to handle potential special characters
    try:
        with open("static/world_map.html", "r", encoding='utf-8') as file:
            html_content = file.read()
    except FileNotFoundError:
        return HTMLResponse(content="Error: world_map.html not found.", status_code=500)
    except Exception as e:
        # Log the error for debugging
        print(f"Error reading world_map.html: {e}")
        return HTMLResponse(content=f"Error reading HTML file: {e}", status_code=500)
    
    # replace placeholder variables with initial airport values
    html_content = html_content.replace("{{ AirportLat }}", str(current_state["airport_lat"]))
    html_content = html_content.replace("{{ AirportLong }}", str(current_state["airport_lon"]))
    html_content = html_content.replace("{{ AirportICAO }}", current_state["airport_icao"])
    
    return HTMLResponse(html_content)

async def send_update(websocket: WebSocket, update_data: dict):
    try:
        await websocket.send_json(update_data)
    except WebSocketDisconnect:
        print("Client disconnected while sending update.")
        active_connections.discard(websocket) # Use discard for safe removal
    except Exception as e:
        print(f"Error sending update: {e}")
        active_connections.discard(websocket) # Remove problematic connection

async def broadcast(message: dict):
    # create a copy to avoid modification issues during iteration
    disconnected_clients = set()
    for connection in active_connections:
        try:
            await connection.send_json(message)
        except WebSocketDisconnect:
            print("Client disconnected during broadcast.")
            disconnected_clients.add(connection)
        except Exception as e:
            print(f"Error broadcasting to a client: {e}")
            disconnected_clients.add(connection)
    # remove disconnected clients outside the loop
    for client in disconnected_clients:
        active_connections.discard(client)

async def handle_airport_update(websocket: WebSocket, airport_code: str):
    print(f"Updating airport to: {airport_code}")
    lat, lon = get_coordinates_airport(airport_code)
    if lat is None or lon is None:
        await send_update(websocket, {"type": "error", "message": f"Could not find coordinates for airport {airport_code}"})
        return

    current_state["airport_icao"] = airport_code
    current_state["airport_lat"] = lat
    current_state["airport_lon"] = lon

    # fetch flights for the new airport - PASS TIME RANGE
    flight_data = fetch_flights(airport_code, DEFAULT_TIME_RANGE_SECONDS)
    
    # broadcast the airport update and flight list to all clients
    update_message = {
        "type": "airport_update",
        "airport_icao": airport_code,
        "coordinates": {"latitude": lat, "longitude": lon},
        "flights": flight_data # contains departures, arrivals, error
    }
    await broadcast(update_message)

async def handle_track_flight(icao24_code: str):
    print(f"Updating tracked flight to: {icao24_code}")
    current_state["tracked_icao24"] = icao24_code.lower() # Ensure lowercase
    # No immediate broadcast needed, tracking loop will pick it up

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.add(websocket)
    print(f"Client connected. Total clients: {len(active_connections)}")

    # send initial state (current airport info and flights)
    # PASS TIME RANGE
    initial_flights = fetch_flights(current_state["airport_icao"], DEFAULT_TIME_RANGE_SECONDS)
    initial_state_message = {
        "type": "initial_state",
        "airport_icao": current_state["airport_icao"],
        "airport_coordinates": {
            "latitude": current_state["airport_lat"],
            "longitude": current_state["airport_lon"]
        },
        "flights": initial_flights,
        "tracked_icao24": current_state["tracked_icao24"]
    }
    await send_update(websocket, initial_state_message)

    try:
        while True:
            # listen for messages from the client (airport change, track flight)
            message_text = await websocket.receive_text()
            message = json.loads(message_text)
            action = message.get("action")

            if action == "update_airport":
                airport_code = message.get("airport_code")
                if airport_code:
                    await handle_airport_update(websocket, airport_code.upper())
                else:
                    await send_update(websocket, {"type": "error", "message": "Missing airport_code for update_airport action"})
            
            elif action == "track_flight":
                icao24 = message.get("icao24")
                if icao24:
                    await handle_track_flight(icao24)
                else:
                    await send_update(websocket, {"type": "error", "message": "Missing icao24 for track_flight action"})
            
            else:
                 await send_update(websocket, {"type": "error", "message": f"Unknown action: {action}"})

    except WebSocketDisconnect:
        print("Client disconnected.")
    except Exception as e:
        print(f"Error in WebSocket connection: {e}")
    finally:
        active_connections.discard(websocket)
        print(f"Client removed. Total clients: {len(active_connections)}")

async def tracking_loop():
    # runs independently to fetch and broadcast plane updates
    while True:
        if current_state["tracked_icao24"]:
            icao = current_state["tracked_icao24"]
            # fetch flight details (this also saves to flight_status.json)
            info = flight_details(icao)

            if info and "Error" not in info:
                 # prepare data to send (only coordinates needed for marker update)
                 plane_update_message = {
                     "type": "plane_update",
                     "icao24": icao,
                     "flight_info": info, # Send full details for popup
                     "coordinates": {
                         "latitude": info.get("Latitude"),
                         "longitude": info.get("Longitude")
                     }
                 }
                 await broadcast(plane_update_message)
            else:
                # optionally send an error if tracking fails repeatedly
                print(f"Could not get details for {icao}: {info.get('Error') if isinstance(info, dict) else 'Unknown error'}")
                # Stop tracking if consistently failing?
                # current_state["tracked_icao24"] = None 
                pass # continue loop for now
        
        # wait before next update
        await asyncio.sleep(10) # update every 10 seconds

@app.on_event("startup")
async def startup_event():
    # start the background tracking loop
    asyncio.create_task(tracking_loop())
    print("Tracking loop started.")

# mount static files (ensure this points to the correct directory)
app.mount("/static", StaticFiles(directory="static"), name="static")
