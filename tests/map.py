#building an interactive world map with folium
import folium 

#set start location and zoom level
world_map = folium.Map(location=[20,20], zoom_start=5)

#saves map to html file
world_map.save("world_map.html")

#testing values for marker - remove later
latitude = 20
longitude = 20
PlaneName = "Plane1"


#create markers (for planes)
folium.Marker(
    location = [latitude, longitude],
    popup= PlaneName,
    icon=folium.Icon(icon="plane"),
).add_to(world_map)

#save changes to map
world_map.save("world_map.html")