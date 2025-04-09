# visualiser
import folium

def create_map(location, zoom_level=5):
    return folium.Map(location=location, zoom_start=zoom_level)

def add_marker(map, latitude, longitude, popup_text):
    folium.Marker(
        location=[latitude, longitude],
        popup=popup_text,
        icon=folium.Icon(icon="plane")
    ).add_to(map)
    
    return map


