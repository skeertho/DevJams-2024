import folium
import geocoder

def get_current_location():
    g = geocoder.ip('me')  
    if g.ok:
        return g.latlng  
    else:
        return None

def handle_location_error():
    print("Error: Your browser doesn't support geolocation or the service failed.")

def init_map():
    default_location = [28.58381, 77.21518]  
    map = folium.Map(location=default_location, zoom_start=15)

    print("Pan to Current Location")

    current_location = get_current_location()
    
    if current_location:
        folium.Marker(current_location, popup="Location found").add_to(map)
        map.location = current_location
        map.zoom_start = 12  
    else:
        handle_location_error()

    map.save("map.html")
    print("Map has been generated. Open 'map.html' to view it.")

init_map()