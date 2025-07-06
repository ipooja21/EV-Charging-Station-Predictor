import folium
import os
from sklearn.cluster import KMeans

def cluster_ev_stations(locations, n_clusters):
    kmeans = KMeans(n_clusters=min(n_clusters, len(locations)), random_state=0, n_init=10)
    kmeans.fit(locations)
    return kmeans.cluster_centers_

def create_map(existing_stations, predicted_stations):
    city_map = folium.Map(location=[existing_stations[0][0], existing_stations[0][1]], zoom_start=12)
    for station in existing_stations:
        folium.Marker(location=[station[0], station[1]], popup="Existing EV Charging Station").add_to(city_map)
    for station in predicted_stations:
        folium.Marker(location=[station[0], station[1]], popup="Predicted EV Charging Station", icon=folium.Icon(color="green")).add_to(city_map)
    map_file_path = os.path.join('static', 'ev_charging_map.html')
    city_map.save(map_file_path)
    return map_file_path
