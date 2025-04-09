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

def plane_marker(map, latitude, longitude, popup_text):
    folium.Marker(
        location=[latitude, longitude],
        popup=popup_text,
        icon=folium.Icon(icon="plane")
    ).add_to(map)

    point1= [latitude, longitude]
    #Frankfurt Airport Co-Ords
    point2 = [50.033333,8.570556]

    #create line between plane and airport
    folium.PolyLine(
    locations=[point1, point2],
    weight=2,  # Line thickness
    color="red",  # Line color
    opacity=0.8  # Line transparency
    ).add_to(map)

    return map